from typing import List


class StudentSentLabEvent:
    def __init__(
        self,
        chat_id: int,
        file_key_id: str,
        same_subject_files_key_ids: List[str],
        lab_work_file_key_id: str
    ):
        self.chat_id = chat_id
        self.file_key_id = file_key_id
        self.same_subject_files_key_ids = same_subject_files_key_ids
        self.lab_work_file_key_id = lab_work_file_key_id

    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание экземпляра из словаря
        """
        return cls(
            chat_id=data.get("chatId"),
            file_key_id=data.get("fileKeyId"),
            same_subject_files_key_ids=data.get("sameSubjectFilesKeyIds", []),
            lab_work_file_key_id=data.get("labWorkFileKeyId")
        )

    def __repr__(self):
        return (
            f"StudentSentLabEvent(chatId={self.chat_id}, "
            f"fileKeyId={self.file_key_id}, "
            f"sameSubjectFilesKeyIds={self.same_subject_files_key_ids}, "
            f"labWorkFileKeyIds={self.lab_work_file_key_id})"
        )
