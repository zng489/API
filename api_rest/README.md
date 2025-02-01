conda activate great_expectations

http://localhost:8000/docs

$ pip install fastapi

$ pip install uvicorn

https://medium.com/@vinicius_/como-criar-uma-api-rest-usando-python-com-fastapi-framework-1701849c0ce6

https://www.youtube.com/watch?v=tpT48Rpt-Ww

https://www.youtube.com/watch?v=XnYYwcOfcn8

https://www.youtube.com/watch?v=wS9LfFtXdBs

uvicorn main:app --reload
    item_dict = jsonable_encoder(db_item)
    db.add(item_dict)
    db.commit()
    db.refresh(item_dict)
    return item_dict
 

# https://medium.com/juntos-somos-mais/fastapi-construindo-microsservi%C3%A7os-de-alta-performance-6f3063e13102
# https://github.com/izaguerreiro/fastapi_techtalk/blob/master/app/schemas.py
# https://github.com/izaguerreiro/fastapi_techtalk/blob/master/app/main.py
# FastAPI app instance


As classes BookCreate e BookResponse em um código FastAPI, ambas derivadas de Pydantic, têm propósitos diferentes, e a existência de duas classes é útil para distinguir entre dados recebidos do cliente e dados enviados para o cliente. Vamos explorar essa diferença:

1. BookCreate:
Uso: Esta classe é usada para definir o esquema dos dados que serão recebidos pelo servidor, geralmente em operações de criação ou atualização de recursos.
Exemplo: Quando você está criando um novo livro na sua aplicação, você só precisa do título e do autor. Nesse caso, BookCreate especifica que esses são os únicos campos que devem ser enviados no corpo da requisição.
python
Copiar código
class BookCreate(BaseModel):
    title: str
    author: str
Contexto: Essa classe define o que o cliente precisa enviar ao servidor quando ele quer criar ou atualizar um livro. Ela não precisa incluir o id, porque o id é geralmente gerado pelo banco de dados.
2. BookResponse:
Uso: Esta classe é usada para definir o esquema dos dados que serão retornados pelo servidor ao cliente. Isso inclui tanto os dados enviados pelo cliente quanto informações adicionais geradas pelo servidor, como o id.
Exemplo: Quando o servidor retorna um livro recém-criado ou atualizado, ele inclui o id no objeto retornado, além dos campos title e author.
python
Copiar código
class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True
Herança: BookResponse herda de BookCreate, o que significa que ele inclui todos os campos de BookCreate (title e author) e adiciona mais campos (id neste caso). Isso é útil porque você evita repetir o mesmo código, mantendo os campos comuns definidos em um só lugar.
Por que ter duas classes?
Separação de Responsabilidades:

BookCreate é para entrada de dados (o que o cliente envia).
BookResponse é para saída de dados (o que o servidor retorna).
Flexibilidade: O esquema dos dados recebidos pelo servidor e os dados retornados ao cliente podem ser diferentes. Por exemplo, o cliente não precisa enviar um id ao criar um livro, mas o id é necessário ao retornar as informações do livro ao cliente.

Evitar Redundância: Usando herança, você evita a duplicação de campos comuns (title, author), mantendo o código mais limpo e fácil de manter.

Resumo:
BookCreate define o que o cliente precisa enviar (ex. ao criar um livro).
BookResponse define o que o servidor retorna, incluindo campos adicionais como id.
Usar duas classes permite que você controle de forma precisa os dados em ambos os fluxos (entrada e saída).