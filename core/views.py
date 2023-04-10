from django.shortcuts import render
from core.forms import FileForm
from django.http import HttpResponse
from .models import File
import boto3
from environ import Env
import boto3
from botocore.exceptions import ClientError
# Create your views here.

# def upload_form(request):
#     if request.method == "POST":
#         form = FileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         else:
#             context = {'form': form}
#             return render(request, 'core/index.html',context)
#     context = {'form': FileForm()}
#     return render(request, 'core/index.html',context)
def upload_form(request):
    env = Env()
    bucket= env('AWS_STORAGE_BUCKET_NAME')
    region = env('AWS_S3_REGION_NAME')
    key = env('AWS_ACCESS_KEY_ID')
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the file to S3 bucket
            file = form.save()
            
            # Generate a pre-signed link for the uploaded file
            s3_client = boto3.client('s3', region_name=region)
            try:
                # Specify the S3 bucket name and key (path) of the uploaded file
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket, 'Key': file.file.name},
                    ExpiresIn=3600  # Link expiration time in seconds (e.g., 1 hour)
                )
            except ClientError as e:
                print(e)
                url = None

            # Pass the pre-signed link to the context for rendering in the modal form
            context = {'form': form, 'presigned_url': url}
            return render(request, 'core/index.html', context)
        else:
            context = {'form': form}
            return render(request, 'core/index.html', context)
    context = {'form': FileForm()}
    return render(request, 'core/index.html', context)


def list_files(request):
    files = File.objects.all()
    context = {'files':files}
    return render(request, 'core/list.html',context)


# def get_url(request):
#     env = Env()
#     bucket= env('AWS_STORAGE_BUCKET_NAME')
#     key = env('AWS_ACCESS_KEY_ID')

#     url = boto3.client('s3').generate_presigned_url(
#     ClientMethod='get_object', 
#     Params={'Bucket': bucket, 'Key': key},
#     ExpiresIn=3600)
#     return render(request, 'core/list.html',context)
    


    url = boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object', 
    Params={'Bucket': 'BUCKET_NAME', 'Key': 'OBJECT_KEY'},
    ExpiresIn=3600)