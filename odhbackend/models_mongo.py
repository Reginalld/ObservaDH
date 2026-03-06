from mongoengine import Document, StringField

class ImagesModel(Document):
    """
    Modelo original do MongoDB para armazenar as imagens em Base64.
    Fica isolado do SQLModel (Postgres) para respeitar a arquitetura NoSQL.
    """
    meta = {
        "collection": "images",
        "indexes": [
            "elasticid",
            # O dev original comentou essa linha
            # {"fields": ["elasticid", "articleposition"], "unique": True}
        ]
    }

    elasticid = StringField(required=True)
    articleposition = StringField(required=True)# Confirmado que é String!
    image = StringField(required=True)# Imagem original (base64)
    caption = StringField(required=True)
    thumb_sd = StringField()# Thumbnail em resolução SD