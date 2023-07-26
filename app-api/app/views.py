from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
import json
from django.core.files.storage import default_storage
import pandas
import re

@csrf_exempt
def validate(request):
    if request.method=='POST':
        file=request.FILES['file']
        data=json.loads(request.POST['rows'])
        print(data)
        #print(JSON.parse(request))
        file_name=default_storage.save(file.name,file)
        csvFile = pandas.read_csv("C:\\Users\\vhars\\Downloads\\hackathon\\app-api\\media\\"+file_name)
        csvHeaders=[]
        for col in csvFile:
            csvHeaders.append(col)

        errors=[]
        numPattern = re.compile(r'^[0-9]*[.,]{0,1}[0-9]*$')

        for items in data:
            if items['type']=="1":
                for index,element in enumerate(csvFile[csvHeaders[items['colNum']-1]]):
                    if(not(isinstance(element, int)) and not(isinstance(element, float))):
                        if not numPattern.match(str(element)):
                            errors.append("Data type not number at line "+str(index+2))
                        
        return JsonResponse({"hello":errors})
