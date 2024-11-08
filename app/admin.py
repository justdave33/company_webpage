from django.contrib import admin
from app.models import GeneralInfo,service, Testimonial, FrequentlyAskedQuestion,ContactFormLog,Blog,Author

# Register your models here.
@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    
    list_display = [
        'company_name',
        'location',
        'email',
        'phone',
        'open_hours',
    ]
    
    
    
@admin.register(service)
class serviceAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
    ]
    
    
    search_fields = [
        "title",
        "description"
    ]
    
    

@admin.register(Testimonial)
class  testimonialAdmin(admin.ModelAdmin):
    list_display = [
        "usernname",
        "user_job_title",
        "display_rating_count"
    ]
    
    
    
    def display_rating_count(self,obj):
        return '*' * obj.rating_count
       
       
    display_rating_count.short_description = 'Rating'    
    


@admin.register(FrequentlyAskedQuestion)
class frequentlyaskedQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "question",
        "answer",
    ]


@admin.register(ContactFormLog)
class ContactFormLogAdmin(admin.ModelAdmin):
    
    list_display = [
        'email',
        'is_ssuccess',
        'is_error',
        'action_time',
      
    ]
    
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj = None):
        return  False
    
    def has_delete_permission(self, request, obj = None):
        return  False
    
    

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
    ]    
    
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    
    list_display = [
        'category',
        'author',
        'title',
        'blog_image',
        'created_at',
      
    ]    