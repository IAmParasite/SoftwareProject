import re
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag,Group,MemberShip,GroupPost, MoviePost, TopicPost
from django.core.paginator import Paginator
from django.contrib import messages

from django.http import HttpResponse
                                            #导入
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from users.models import User
from django.utils import timezone
from guardian.shortcuts import assign
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_users_with_perms
from guardian.shortcuts import get_objects_for_user
def login(request):
    if request.method=='POST':
        user = authenticate(request,username=request.POST['用户名'],password=request.POST['密码'])
        if user is None:
            return render(request, 'forum/login.html',{'错误':'用户名不存在！'})
        else:
            login(request,user)
            return rerdirect('forum:index')
    else:
        return render(request,'forum/login.html')

def register(request):
    if request.method=='POST':
        rf = UserCreationForm(request.POST)
        if rf.is_valid():
            user = authenticate(username=rf.cleaned_data['username'],password=rf.cleaned_data['password'])
            login(request, user)
            return rerdirect('forum:index')
    else:
        rf=UserCreationForm()
    content = {'注册表单': rf}
    return render(request,'forum/register.html',content)


class IndexView(ListView):
    model = Post        ## 告诉 django 我们要取的数据库模型是class Post, 
    template_name = 'forum/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class BooksIndexView(ListView):
    model = Post        ## 告诉 django 我们要取的数据库模型是class Post, 这里其实应该命名为Books
    template_name = 'forum/books_index.html'    
    context_object_name = 'books_list'
    #paginate_by = 10

# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'forum/book_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
        
        #添加为小组成员
def add_group(request,pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            group_now  = Group.objects.filter(pk = pk).first()
            user_now = User.objects.filter(username=request.user.username).first()
            mm = MemberShip.objects.filter(person=user_now,group=group_now)
            if not mm:
                m1=MemberShip.objects.create(person=user_now,group=group_now,date_join=timezone.now())
            return redirect('forum:groups_index')

        else:
            return render(request,'registration/login.html',{'错误':'还未登录！'})
    else:
        return render(request,'forum/login.html')
##管理员添加
def add_groupmanager(request,name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            group_now  = Group.objects.filter(name = name).first()
            user_now = User.objects.filter(username=request.user.username).first()
            gg = GroupPost.objects.filter(group=group_now)
            if  group_now:
                for gp in gg:
                    assign_perm('grouppost_delete',user_now, gp)
            return redirect('forum:groups_index')

        else:
            return render(request,'registration/login.html',{'错误':'还未登录！'})
    else:
        return render(request,'forum/login.html')
        
    
class GroupsIndexView(ListView):
    model = Group        ## 告诉 django 我们要取的数据库模型是class GroupPost,
    template_name = 'forum/groups_index.html'
    context_object_name = 'groups_list'

#paginate_by = 10

class GroupPostView(ListView):
    model = GroupPost
    template_name = 'forum/group_detail.html'
    context_object_name = 'group_post'
    def get_queryset(self):
        c = Group.objects.filter(pk=self.kwargs['pk']).first()
        
        return GroupPost.objects.filter(group=c).order_by('created_time')
        
            
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
#        md = markdown.Markdown(extensions=[
#            'markdown.extensions.extra',
#            'markdown.extensions.codehilite',
#            TocExtension(slugify=slugify),
#        ])
#        post.members = md.convert(post.members)
#        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#        post.toc = m.group(1) if m is not None else ''
        return post
        

class GroupDetailView(DetailView):
# 这些属性的含义和 ListView 是一样的
    model = GroupPost
    template_name = 'forum/group_detailmore.html'
    context_object_name = 'grouppost'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(GroupDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post

class MoviesIndexView(ListView):
    model = MoviePost        ## 告诉 django 我们要取的数据库模型是class Post, 
    template_name = 'forum/movies_index.html'
    context_object_name = 'movies_list'
    #paginate_by = 10
class MoviePostDetailView(DetailView):
    model = MoviePost 
    template_name = 'forum/movie_detail.html'
    context_object_name = 'movie_post'
    def get(self, request, *args, **kwargs):
        response = super(MoviePostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


class PostDetailView(DetailView):
# 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'forum/book_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
class TopicIndexView(ListView):
    model = TopicPost        ## 告诉 django 我们要取的数据库模型是class Post,
    template_name = 'forum/topic_index.html'
    context_object_name = 'topic_list'
    #paginate_by = 10
class TopicPostDetailView(DetailView):
    model = TopicPost
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic_post'
    def get(self, request, *args, **kwargs):
        response = super(TopicPostDetailView, self).get(request, *args, **kwargs)
        # self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=t)
