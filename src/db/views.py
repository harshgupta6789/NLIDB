from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Database
from .serializers import DatabaseSerializer
import urllib.parse
from .nlp.nlidb import *

import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


# Create your views here.

class DatabaseAPI(APIView):

    def get(self, request):
        # database = Database.objects.all()
        # serializer = DatabaseSerializer(database, many=True)
        hindi_sentence = self.request.query_params.get('hindi_sentence')

        if hindi_sentence is None:
            return Response('Invalid parameters')

        hindi_sentence = urllib.parse.unquote(hindi_sentence)

        try:
            result = perform_nlidb(hindi_sentence)
        except RuntimeError:
            result = {'error': True}

        return Response(result)

    def post(self):
        pass
