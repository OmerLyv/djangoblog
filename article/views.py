from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article,Comment
from .decorators import user_is_entry_author
from django.db.models import Count

from django.contrib import messages #ekrana mesaj yazdırmak için gerekli modül
# Create your views here.

#Anasayfa
def index(request):

    return render(request,"index.html") #templates klasörünün içindeki article'ın içindeki index.html sayfasını renderlıyor çalıştırıyor.

def about(request):
    return render(request,"about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)  #Kontrol panelinde o an hangi kullanıcı varsa onun makalelerini gösteriyor

    context ={"articles":articles}       


    return render(request,"dashboard.html",context) 

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)  #Makaleyi formdaki bilgilere göre oluşturuyor ve commit false diyerek biz save yaptırmıyoruz. Çünki ıd ve username atayacağız
        article.author = request.user #makaleye yazar bilgisini verdik
        article.save()
        messages.success(request,"Makaleniz Oluşturuldu")
        return redirect("article:dashboard")
    return render(request,"addarticle.html",{"form":form}) 

def detail(request,id):   #Dashboardda makale başlığına tıklandığında makalenin id sine göre id yi db den filtreleyip detail htmline gönderiyoruz clienti

    article = get_object_or_404(Article,id = id)
    comments = article.comments.all()
    comments_count = comments.count
    
    return render(request,"detail.html",{"article":article,"comments":comments,"comments_count":comments_count})

@login_required(login_url="user:login")
@user_is_entry_author
def updateArticle(request,id):

    article = get_object_or_404(Article,id = id)
    form =ArticleForm(request.POST or None,request.FILES or None,instance=article)
    if form.is_valid():
        article = form.save(commit=False)  #Makaleyi formdaki bilgilere göre oluşturuyor ve commit false diyerek biz save yaptırmıyoruz. Çünki ıd ve username atayacağız
        article.author = request.user #makaleye yazar bilgisini verdik
        article.save()
        messages.success(request,"Makaleniz Güncellendi")
        return redirect("article:dashboard") 
    return render(request,"update.html",{"form":form})
    
@login_required(login_url="user:login")
@user_is_entry_author
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request,"Makaleniz Silindi")
    return redirect("article:dashboard")


def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})

    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})


def addComment(request,id):
    article=get_object_or_404(Article,id=id)   #id si id olan postu yani article'ı alıyoruz
    if request.method =="POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment =  Comment(comment_content=comment_content,comment_author=comment_author)
        newComment.article=article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))


    