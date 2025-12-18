#include<stdio.h>
#include<stdlib.h>
#include<stdarg.h>
#include<sys/mman.h>
#define EXIT_COND -1

enum{
  LPAREN,
  RPAREN,
  LAMBDA,
  DOT,
  LCID
};

char *tokens[]={"(",")","λ",".","[A-Z]"};
static int token_array[2];
static int token_type=0;
static int token_counter=0;

int is_space(char c){
  if(c == '\t' || c == ' ' || c == '\n')
    return 1;
  else
    return 0;
}

int gettok(){
  void error(char *fmt,...);
  int c;
  while((c=getchar()) == '\t'  || c == ' ');
  switch(c){
  case '(':
    token_array[token_counter++]=c;
    return token_type=LPAREN;
  case ')':
    token_array[token_counter++]=c;
    return token_type=RPAREN;
  case '.':
    token_array[token_counter++]=c;
    return token_type=DOT;
  case '#':
    token_array[token_counter++]=c;
    return token_type=LAMBDA;
  default:    
    if((c >= 'a' &&  c <= 'z') || (c >= 'A' && c <= 'Z')){
      token_array[token_counter++]=c;
      return token_type=LCID;
    }else if(is_space(c) || c == EOF){
      token_type=EXIT_COND;
      return  -1;
    }else{
      error("unexpected token %c\n",c);
      exit(-1);
    }
  }
}

void error(char *fmt,...){
  va_list ap;
  va_start(ap,fmt);
  vfprintf(stderr,fmt,ap);
  va_end(ap);
}

#define LEXER_ERR 0
int next(char type){
  if(token_counter != 1){
    if(gettok() == type)
      return 1;
  }else if(token_counter == 1){
    if(type == token_type)
      return 1;
  }
  if(token_type == EXIT_COND)
    token_counter = 1;
 
  return LEXER_ERR;
}

int skip(char type){
  if(next(type)){
    --token_counter;
    return 1;
  }
  return 0;
}

int match(char type){
  void expect_tok(char);
  if(next(type))
     --token_counter;
  else
    expect_tok(type);
  return 1;
 }

void expect_tok(char type){
  error("expected token %s ",tokens[type]);
  error("token found  %c \n",token_array[--token_counter]);
  exit(-1);
}

int token(char type){
  if(next(type)){
    return token_array[--token_counter];
  }
  return LEXER_ERR;
}

/*------------ parser part -------------*/

enum{
  IDENTIFIER=01750,
  ABSTRACTION=03740,
  APPLICATION=05670
};

enum{
  FREE,
  BOUND
};

typedef struct node{
  int kind;
  union{
    struct node  *next;
    struct {
      int val;
      int ctx_length;
      int type_var;
    };
    struct{
      char param;
      struct node *body;
    };
    struct{
      struct node *lhs;
      struct node *rhs;
    };
  };
}node;

/* variable storage  depending on whether free or not */
#define MAX_VARS 30
static char free_variables[MAX_VARS];
static char bound_variables[MAX_VARS];
static int fp=0;
static int bp=0;

#define KiloByte(x) ((1ull << 10) * (x))

struct interpreter_alloc{
  void *interpreter_storage;
  int  interpreter_storage_size;
};

int get_interpreter_storage(struct interpreter_alloc *interpreter_storage,unsigned bytes){
  interpreter_storage->interpreter_storage_size=bytes;
  interpreter_storage->interpreter_storage= mmap(NULL,interpreter_storage->interpreter_storage_size,PROT_READ|PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS,
                  -1, 0);
  if(interpreter_storage->interpreter_storage){
    return 1;
  }
  return 0;
}

/* parser storage */

typedef struct{
  void *buffer;
  size_t  offset;
  size_t capacity;
}parser_block;

void *parser_block_push(parser_block *block,size_t size){
  void *ptr=NULL;
  if((block->offset + size ) <= block->capacity){
    ptr=(block->buffer + block->offset);
    block->offset += size;
  }
  return ptr;
}

#define PushStruct(block,type) (type *)parser_block_push(block,sizeof (type))
void parser_alloc(struct interpreter_alloc *interpreter_storage,parser_block *node_parser_block,parser_block  *ctx_parser_block){
  node_parser_block->buffer=interpreter_storage->interpreter_storage;
  node_parser_block->offset=0;
  node_parser_block->capacity=KiloByte(8);
  ctx_parser_block->buffer=(interpreter_storage->interpreter_storage + KiloByte(8));
  ctx_parser_block->offset=0;
  ctx_parser_block->capacity=KiloByte(8);
}

void  parser_release(parser_block *block){
  block->offset=0;
}
//specific to type to support free list mechanism
typedef struct parser_block_state{
  parser_block *block;
  struct node *free_node;
}parser_block_state;

node *node_alloc(struct parser_block_state *state){
  node zero={0};
  node *result=state->free_node;
  if(result != NULL){
    state->free_node=state->free_node->next;
    *result=zero;
  }else{
    result=PushStruct(state->block,node);
  }
  return result;
}

void node_release(struct parser_block_state *state,node *t){
  t->next=state->free_node;
  state->free_node=t;
}

/* tracking  de brujin indices  */
typedef struct ctx_node{
  int key;
  struct ctx_node *next;
}ctx_node;

typedef struct ctx_header{
  int count;
  struct ctx_node *head;
  struct ctx_node *z;
}ctx_header;

struct ctx_node *t;

void ctx_list_init(ctx_header *header,parser_block  *ctx_parser_block){
  header->head=PushStruct(ctx_parser_block,ctx_node);
  header->z=PushStruct(ctx_parser_block,ctx_node);
  header->count=0;
  header->head->next=header->z;
  header->z->next=header->z;
}

void push_ctx_list(char c,ctx_header *header,parser_block  *ctx_parser_block){
  bound_variables[bp++]=c;
  t=PushStruct(ctx_parser_block,ctx_node);
  t->key=c;
  t->next=header->head->next;
  header->head->next=t;
  header->count++;
}

struct ctx_var{
  int val;
  int ctx_length;
};

int get_key_idx(char c,ctx_header *header,struct ctx_var *result){
  t=header->head->next;
  for(int idx=0; t != header->z; t=t->next,idx++){
    if(c == t->key){
      result->val=idx;
      result->ctx_length=((header->count-1) - idx);
      return 1;
    }
  }
 
  free_variables[fp++]=c;
  return 0;
}

int get_free_ctx(){
  int temp=fp;
  return --temp;
}

node *term(ctx_header *,parser_block_state *,parser_block  *);
node *atom(ctx_header *,parser_block_state *,parser_block  *);
node *application(ctx_header *,parser_block_state *,parser_block  *);

node *term(ctx_header *header,parser_block_state *node_block,parser_block  *ctx_parser_block){
    if(skip(LAMBDA)){
    char id=token(LCID);
    push_ctx_list(id,header,ctx_parser_block);
    match(DOT);
    node *temp=term(header,node_block,ctx_parser_block);
    node *abstraction=node_alloc(node_block);
    abstraction->kind=ABSTRACTION;
    abstraction->param=id;
    abstraction->body=temp;
    return abstraction;
    }else{
    return application(header,node_block,ctx_parser_block);
  }
  
}

node *application(ctx_header *header,parser_block_state *node_block,parser_block  *ctx_parser_block){
  node *lhs=atom(header,node_block,ctx_parser_block);
  for(;;){
    node *rhs=atom(header,node_block,ctx_parser_block);
    if(!rhs){
      return lhs;
    }
    node *application=node_alloc(node_block);
    application->kind=APPLICATION;
    application->lhs=lhs;
    application->rhs=rhs;
    lhs=application;
  }

}

node *atom(ctx_header *header,parser_block_state *node_block,parser_block  *ctx_parser_block){
  if(skip(LPAREN)){
    node *temp=term(header,node_block,ctx_parser_block);
    match(RPAREN);
    return temp;
  }else if(next(LCID)){
    node *identifier=node_alloc(node_block);
    identifier->kind=IDENTIFIER;
    char id=token(LCID);
    struct ctx_var result={0};
    if(get_key_idx(id,header,&result)){
      identifier->val=result.val;
      identifier->ctx_length=result.ctx_length;
      identifier->type_var=BOUND;
    }else{
      identifier->val=get_free_ctx();
      identifier->ctx_length=get_free_ctx();
      identifier->type_var=FREE;
    }
    return identifier;
  }
  return NULL;
}

void print_eval(node *root){
  if(root->kind == APPLICATION){
    print_eval(root->lhs);
    print_eval(root->rhs);
  }else if(root->kind == ABSTRACTION){
    printf("(λ%c.",root->param);
    print_eval(root->body);
    printf(")");
  }else{
    if(root->type_var == FREE){
      printf("%c",free_variables[root->ctx_length]);
    }else{
       printf("%c",bound_variables[root->ctx_length]);
    }
  }

}

node *shift(node *N,int shamt,int cutoff,parser_block_state *node_block){
   if(N->kind == IDENTIFIER){
    node *identifier=node_alloc(node_block);
    identifier->kind=IDENTIFIER;
    if(N->val >= cutoff)
      identifier->val= (N->val + shamt);
    else
      identifier->val=N->val; 
    identifier->ctx_length=N->ctx_length;
    identifier->type_var=N->type_var;
    return identifier;
  }else if(N->kind == ABSTRACTION){
    node *abstraction=node_alloc(node_block);
    abstraction->kind=ABSTRACTION;
    abstraction->param=N->param;
    abstraction->body=shift(N->body,shamt,cutoff + 1,node_block);
    return  abstraction;
  }else if(N->kind == APPLICATION){
    node *application=node_alloc(node_block);
    application->kind=APPLICATION;
    application->lhs=shift(N->lhs,shamt,cutoff ,node_block);
    application->rhs=shift(N->rhs,shamt,cutoff ,node_block);
    return application;
  }
  return NULL;
}

int label_captures(node *M,node *N){
  if(N->kind ==IDENTIFIER && N->type_var == BOUND)
    if(M->param == bound_variables[N->ctx_length])
      return 1;
   return 0;
 }

node *substitute(node *M,node *N,int binders,parser_block_state *node_block){
    if(M->kind == IDENTIFIER){
      if(M->type_var == FREE)
	return M;
      if(M->val >= binders)
	return shift(N,binders,0,node_block);
      else
	return M;
  }else if(M->kind == ABSTRACTION){
    node *abstraction=node_alloc(node_block);
    abstraction->kind=ABSTRACTION;
    abstraction->param=M->param;
    if(label_captures(M,N))
      abstraction->param='S';
    abstraction->body=substitute(M->body,N,binders+1,node_block);
    return  abstraction;
  }else if(M->kind == APPLICATION){
    node *application=node_alloc(node_block);
    application->kind=APPLICATION;
    application->lhs=substitute(M->lhs,N,binders,node_block);
    application->rhs=substitute(M->rhs,N,binders,node_block);
    return application;
   }
  return NULL;
}

node *reduce_once(node *t,parser_block_state *node_block){
  if(t->kind == APPLICATION){
    if(t->lhs->kind == ABSTRACTION){
      return shift(substitute(t->lhs->body,shift(t->rhs,1,0,node_block),0,node_block),-1,0,node_block);
    }
    node *temp=reduce_once(t->lhs,node_block);
    if(temp !=  t->lhs){
    node *application=node_alloc(node_block);
    application->kind=APPLICATION;
    application->lhs=temp;
    application->rhs=t->rhs;
    return application;
    }
    temp=reduce_once(t->rhs,node_block);
    if(temp != t->rhs){
    node *application=node_alloc(node_block);
    application->kind=APPLICATION;
    application->lhs=t->lhs;
    application->rhs=temp;
    return application;
    }
    return t;
  }else{
    return t;
  }
}

node *eval(node *root,parser_block_state *node_block){
  for(;;){
    node *temp=reduce_once(root,node_block);
    if(temp != root){
      root=temp;
    }else{
      return root;
    }
  }
}

int  interpreter(parser_block *node_block,parser_block *ctx_block){
  parser_block_state parser_block_state={0};
  parser_block_state.block=node_block;
  parser_block_state.free_node=NULL;
  ctx_header header={0};
  ctx_list_init(&header,ctx_block);
  node *root=term(&header,&parser_block_state,ctx_block);
  printf("Expression:");
  print_eval(root);
  node *evaluated=eval(root,&parser_block_state);
  printf("\nEval:");
  print_eval(evaluated);
  printf("\n");
  fp=0;
  bp=0;
  token_counter=0;
  parser_release(node_block);
  parser_release(ctx_block);
  return 1;
}

int main(){
  char  c;
  struct interpreter_alloc interpreter_storage={0};  
  parser_block node_block={0};
  parser_block ctx_block={0};
  if(get_interpreter_storage(&interpreter_storage,KiloByte(16))){
    parser_alloc(&interpreter_storage,&node_block,&ctx_block);
  }else{
        printf("Alloc error\n");
	exit(-1);
  }
    L: printf("Input expression (# for lambda abstraction) and  press Enter for evaluation \n");
    if(interpreter(&node_block,&ctx_block)){
      printf("press y to continue and q to stop\n");
      scanf(" %c",&c);
      if(c == 'q'){
	return 0;
      }else if(c == 'y'){
	scanf("%c",&c); 
	if(c == '\n')
	  goto L;
	else
	  goto E;
      }else{
      E:printf("Invalid input %c : find usage\n",c);
	exit(-1);
      }
    }
    return 0;
}
