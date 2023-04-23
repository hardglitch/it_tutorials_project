from copy import deepcopy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.dictionary.models import Dictionary
from src.dictionary.schemas import DictionaryScheme


async def add_word(
        word: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool:

    if not word or not async_session: return False

    async with async_session as session:
        try:
            new_word = Dictionary(
                lang_code=word.lang_code,
                value=word.value
            )
            session.add(new_word)
            await session.commit()
            await session.refresh(new_word)
            return True

        except Exception:
            raise


async def edit_word(
        word: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not word or not async_session or not word.word_code: return False

    async with async_session as session:
        try:
            word_from_db: DictionaryScheme | None = await session.get(Dictionary, word.word_code)
            if not word_from_db: return False

            word_from_db_snapshot = deepcopy(word_from_db)

            if word.lang_code and word.lang_code != word_from_db.lang:
                word_from_db.lang = word.lang_code
            if word.value and word.value != word_from_db.value:
                word_from_db.value = word.value

            if word_from_db.lang != word_from_db_snapshot.lang_code or \
               word_from_db.value != word_from_db_snapshot.value:

                session.add(word_from_db)
                await session.commit()
                return True
            else:
                return False

        except Exception:
            raise
