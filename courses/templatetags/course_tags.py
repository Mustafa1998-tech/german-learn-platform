from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """Convert YouTube URL to embed format"""
    if not url:
        return ""
    # If already in embed format
    if 'youtube.com/embed/' in url:
        return url
    # Convert watch URL
    if 'youtube.com/watch' in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    # Convert youtu.be URL
    if 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[-1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    return url

@register.filter
def youtube_thumbnail(video_id):
    """Generate YouTube thumbnail URL from video ID"""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

@register.filter
def split_by_semicolon(value):
    """Split a string by semicolon and return as list"""
    if not value:
        return []
    return [item.strip() for item in value.split(';') if item.strip()]

@register.filter
def format_duration(minutes):
    """Format duration in minutes to HH:MM format"""
    if not minutes:
        return ""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins:02d}m"
    return f"{mins} min"

@register.filter
def highlight_search(text, search_term):
    """Highlight search terms in text"""
    if not search_term or not text:
        return text
    pattern = re.compile(f'({re.escape(search_term)})', re.IGNORECASE)
    return mark_safe(pattern.sub(r'<span class="highlight">\1</span>', str(text)))
