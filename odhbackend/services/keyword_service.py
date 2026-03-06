import random
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from odhbackend.models import KeywordList 

class KeyWordsServices:
    def __init__(self, db: Session):
        self.db = db

    def add_keyword_list(self, user_id: str, keyword: str) -> dict:
        if not keyword.strip():
            return {"status": "error", "message": "A palavra-chave não pode estar vazia."}

        existing_keyword = self.db.query(KeywordList).filter(
            KeywordList.user_id == user_id,
            KeywordList.keyword == keyword
        ).first()

        if existing_keyword:
            return {"status": "error", "message": "Palavra-chave já existe para este usuário."}

        try:
            new_keyword = KeywordList(keyword=keyword, user_id=user_id)
            self.db.add(new_keyword)
            self.db.commit()
            self.db.refresh(new_keyword)
            return {
                "status": "success",
                "keyword_id": new_keyword.id,
                "keyword": keyword
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {"status": "error", "message": f"Erro interno: {str(e)}"}

    def delete_keyword(self, user_id: str, keyword: str) -> dict:
        existing_keyword = self.db.query(KeywordList).filter(
            KeywordList.user_id == user_id,
            KeywordList.keyword == keyword
        ).first()

        if not existing_keyword:
            return {"status": "error", "message": "Palavra-chave não encontrada."}

        try:
            self.db.delete(existing_keyword)
            self.db.commit()
            return {"status": "success", "message": "Palavra-chave deletada."}
        except SQLAlchemyError as e:
            self.db.rollback()
            return {"status": "error", "message": f"Erro interno: {str(e)}"}

    def get_keywords_for_user(self, user_id: str) -> List[str]:
        """
        AR01: A função que o nosso ArticleService usa como Fallback!
        """
        keywords = self.db.query(KeywordList).filter(KeywordList.user_id == user_id).all()
        return [k.keyword for k in keywords]

    def get_all_unique_keywords(self) -> List[str]:
        try:
            keywords = self.db.query(KeywordList.keyword).all()
            
            unique_keywords = {k[0] for k in keywords} 
            
            unique_keywords_list = list(unique_keywords)
            random.shuffle(unique_keywords_list)
            
            return unique_keywords_list

        except SQLAlchemyError as e:
            print(f"Erro ao buscar palavras únicas: {str(e)}")
            return []