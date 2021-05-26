from django.db import models

from base.models import BaseModel

from profiles.models import Profile

from proof.utilities import get_proof_upload_path


class Proof(BaseModel):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_proof_upload_path)

    def __str__(self):
        return self.file.name
