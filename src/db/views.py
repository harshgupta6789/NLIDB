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
from pathlib import Path

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


# Create your views here.

class DatabaseAPI(APIView):

    def get(self, request):
        # database = Database.objects.all()
        # serializer = DatabaseSerializer(database, many=True)
        hindi_sentence = self.request.query_params.get('query')

        if hindi_sentence is None:
            return Response({'error': 'Invalid Parameters'})

        hindi_sentence = urllib.parse.unquote(hindi_sentence)

        my_path = Path('./database/db.sql')
        if not my_path.is_file():
            return Response({"error": "Database does not exists"})

        try:
            result = perform_nlidb(hindi_sentence)
        except:
            result = {'error': "Unexpected Error Occurred"}

        if "error" not in result:
            for k, v in result.items():
                if type(result[k]) == str:
                    result[k] = str(v).encode('utf-8')
                elif type(result[k]) == bool:
                    result[k] = result[k]
                elif type(result[k]) == list:
                    temp = []
                    for items in result[k]:
                        if type(items) == list:
                            temp2 = []
                            for item in items:
                                temp2.append(str(item).encode('utf-8'))
                            temp.append(temp2)
                        else:
                            temp.append(str(items).encode('utf-8'))
        return Response(result)

    def post(self):
        pass
