from .models import Level, Lesson

def course_levels(request):
    """Make levels available in all templates"""
    return {
        'all_levels': Level.objects.all().order_by('order')
    }

def featured_lessons(request):
    """Get featured lessons for the homepage"""
    return {
        'featured_lessons': Lesson.objects.filter(
            is_featured=True, 
            is_free=True
        ).select_related('level').order_by('?')[:6]
    }

def user_progress(request):
    """Get user progress if authenticated"""
    if not request.user.is_authenticated:
        return {}
        
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return {
        'user_profile': profile,
        'user_completed_lessons': set(profile.completed_lessons.values_list('id', flat=True))
    }
