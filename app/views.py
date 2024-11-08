from django.shortcuts import render, redirect
from django.core.mail import send_mail
from app.models import GeneralInfo, service, Testimonial, FrequentlyAskedQuestion, ContactFormLog,Blog
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

def index(request):
    general_info = GeneralInfo.objects.first()
    services = service.objects.all()
    testimonials = Testimonial.objects.all()
    faqs = FrequentlyAskedQuestion.objects.all()
    recent_blogs = Blog.objects.all().order_by("-created_at")[:3]
    for blog in recent_blogs:
        print(f"blog : {blog}" )
        print(f"blog.created_at: {blog.created_at}")
        print(f"blog.author: {blog.author}")
        print(f"blog.author.country: {blog.author.country}")
        print("")
        
        
        
    default_value= ""
    
    context = {
        "company_name": getattr( general_info,"company_name", default_value),
        "location": getattr( general_info,"location", default_value),
        "email": getattr( general_info,"email", default_value),
        "phone": getattr( general_info,"phone", default_value),
        "open_hours": getattr( general_info,"open_hours", default_value),
        "video_url": getattr( general_info,"video_url", default_value),
        "twitter_url": getattr( general_info,"twitter_url", default_value),
        "facebook_url": getattr( general_info,"facebook_url", default_value),
        "instagram_url": getattr( general_info,"instagram_url", default_value),
        "linkedin_url": getattr( general_info,"linkdin_url", default_value),
        "services": getattr( general_info,"services", default_value),
        "testimonials": getattr( general_info,"testimonials", default_value),
        "faqs": getattr( general_info,"faqs", default_value),
        "recent_blogs": getattr( general_info,"recent_blogs", default_value),
    }
    return render(request, "index.html", context)

def contact_form(request):
    if request.method == 'POST':
        print("\nUser has submitted a contact form\n")
        print(f"request.POST: {request.POST}")

        # Collect data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        context = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
        }
        html_content = render_to_string('email.html', context)
        
        # Set initial values for email status
        is_ssuccess = False
        is_error = False
        error_message = ""
        
        try:
            # Attempt to send the email
            send_mail(
                subject=subject,
                message=None,
                html_message=html_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except Exception as e:
            # Handle any errors in sending email
            is_error = True
            error_message = str(e)
            messages.error(request, "There is an error, could not send email")
        else:
            # If email is sent successfully
            is_ssuccess = True
            messages.success(request, "Email has been sent")
        
        # Clear messages after setting them
        list(messages.get_messages(request))
        
        # Log the form submission
        ContactFormLog.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            action_time=timezone.now(),
            is_ssuccess=is_ssuccess,
            is_error=is_error,
            error_message=error_message
        )
        
        return redirect('contact_form')
    

def blog_detail(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    
    recent_blogs = Blog.objects.all().exclude(id=blog_id).order_by("-created_at")[:2]
    
    context = {
        "blog":blog,
        "recent_blogs": recent_blogs,
    }
    return render(request, "blog_detail.html", context)
    
    
    
def blogs(request):
    all_blogs = Blog.objects.all().order_by("-created_at")
    blogs_per_page = 2
    paginator = Paginator(all_blogs, blogs_per_page)
    
    print(f"paginator.num_pages : {paginator.num_pages}")
    page = request.GET.get('page')
    
    print(f"page : {page}")
    
    try:
        blogs = paginator.page(page)
        
    except PageNotAnInteger:
        blogs = paginator.page(1) 
        
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    
    context = {
        "blogs": blogs,
    }
    
    return render(request, "blogs.html", context)
   
