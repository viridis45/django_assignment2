#from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db.models import Sum
from .serializers import *
from .models import *

import pdb

tester = status.HTTP_200_OK


@api_view(['POST'])
@permission_classes([AllowAny,])
def signin(request):
    if request.method == 'POST':
        try:
            serializer = NewUserSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            result = {
                'result':'suc',
                'message':f'created {serializer.data["username"]}',
                'user':serializer.data            
                }
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as exp:
            result = {
                'result' : 'error',
                'message' : str(exp)
                }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)       






@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        try:
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                result = {
                    'result':'success',
                    'message':'Login successful',
                    'user': serializer.data
                    }
                status = status.HTTP_200_OK
                return Response(result, status=status)
            else:
                result = {
                    'result' : 'error',
                    'message' : 'Login failed. User information does not exist'}
                status = HTTP_400_BAD_REQUEST
                return Response(result, status=status)
        except Exception as exp:
            result = {
                'result' : 'error',
                'message' : 'error'}
            status = HTTP_400_BAD_REQUEST
            return Response(result, status=status)
        
@api_view(['GET'])
def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            result = {'result' : 'success',
                    'message' : 'Logout successful'}
            #status = HTTP_200_OK
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'result' : 'error',
                'message' : 'Login not successful'}
            status = HTTP_400_BAD_REQUEST
            return Response(result, status=status)



from rest_framework import status

@api_view(['GET','POST'])
def entry(request):
    if request.method == 'GET':
        entries = EntryModel.objects.filter(owner=request.user.username, pre_delete=False)
        tot_exp = entries.aggregate(Sum('amount')).get('amount__sum', 0.00)
        result = {
            'result':'success',
            'data' : tot_exp
        }

        return Response(result, status = status.HTTP_202_ACCEPTED)
        # return render(request, 'entry.html', {'ent':entries, 'tot_exp':tot_exp})
        
    elif request.method == 'POST':
        try:
            if request.user.is_authenticated:
                serializer=EntrySerializer(data=request.POST)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(owner=request.user)
                # return redirect(reverse('usr:entry'))
            else:
                result = {
                    'result' : 'error',
                    'message' : ''
                    }
            status = HTTP_400_BAD_REQUEST
            return Response(result, status=status)

                # return HttpResponse('user not logged in')
        except Exception as exp:
            return
            # return HttpResponse(f'exp: {exp}') 
        
        
# class Deleteds(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             deleteds = EntryModel.objects.filter(owner=request.user.username).filter(pre_delete=True)
#             return render(request, 'entry_deleted.html', {'ent':deleteds})
#         else:
#             return redirect('usr:login')



# @login_required()
# def entry_delete(request, entry_id):
#     entry = EntryModel.objects.get(pk=entry_id)
#     if request.user.username == entry.owner:
#         if entry.pre_delete == True:
#             entry.delete()
#         else:
#             entry.pre_delete = True
#             entry.save()
#         return redirect(reverse('usr:entry'))
#     else:
#         return HttpResponse('Incorrect usr')
    
# @login_required()
# def entry_revert(request, entry_id):
#     entry = EntryModel.objects.get(pk=entry_id)
#     if request.user.username == entry.owner:
#         if entry.pre_delete == True:
#             entry.delete()
#         else:
#             entry.pre_delete = True
#             entry.save()
#         return redirect(reverse('usr:entry'))
#     else:
#         return HttpResponse('Incorrect usr')
    

# @login_required()
# def entry_get(request, entry_id):
#     entries = EntryModel.objects.get(id=entry_id)
#     entries.date = entries.date.strftime('%Y-%m-%d')
#     return TemplateResponse(request, 'entry_edit.html', {'ent':entries})

# @login_required()
# def entry_put(request, entry_id):
#     try:
#         if request.method =='POST':
#             entry = EntryModel.objects.get(id=entry_id)
#             if request.user.username == entry.owner:
#                 serializer=EntrySerializer(entry, data=request.POST)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save(owner=request.user.username)
#                     return redirect(reverse('usr:entry'))
#                 return HttpResponse('wrong format')
#             return HttpResponse(f'not owner, {request.user} != {entry.owner}')
    
#     except Exception as exp:
#         return HttpResponse(f'exp: {exp}')
