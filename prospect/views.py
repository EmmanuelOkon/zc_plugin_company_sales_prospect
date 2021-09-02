from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ProspectSerializer
import requests, json
import pandas as pd
# Create your views here.

class ProspectsDetailView(APIView):

    serializer_class = ProspectSerializer
    queryset = None

    def get(self, request, *args, **kwargs):

        url = "https://zccore.herokuapp.com/data/read/000000000000000000000000/prospects/612a3a914acf115e685df8e3/"
        response = requests.request("GET", url)
        r = response.json()
        if response.status_code == 200:

            dataframe = pd.DataFrame(r['data'])
            dataframe.set_index('_id', inplace=True)
            detail_prospect_data = json.loads(dataframe.loc[kwargs["id"], :].to_json())
            detail_prospect_data['_id'] = kwargs["id"]

            serializer = ProspectSerializer(data=detail_prospect_data, many=False)
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)