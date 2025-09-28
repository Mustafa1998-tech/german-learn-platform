from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Level, Lesson, Exercise, Result,
    FlashcardDeck, Flashcard, UserProfile,
    Achievement, Discussion, Comment, UserFlashcardProgress
)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'description_short')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if obj.description else ''
    description_short.short_description = 'Description'

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1
    fields = ('type', 'question', 'options', 'answer', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'difficulty', 'is_free', 'is_featured', 'order', 'youtube_preview', 'created_at')
    list_filter = ('level', 'difficulty', 'is_free', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'translation', 'short_description')
    list_editable = ('is_free', 'is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExerciseInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'level', 'difficulty', 'short_description', 'content', 'translation')
        }),
        ('Media', {
            'fields': ('youtube_url', 'audio_file', 'thumbnail', 'duration_minutes'),
            'classes': ('collapse',)
        }),
        ('Vocab & Grammar', {
            'fields': ('vocab', 'grammar_points'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_free', 'is_featured', 'order'),
            'classes': ('collapse',)
        }),
    )
    
    def youtube_preview(self, obj):
        if obj.youtube_url:
            video_id = obj.youtube_url.split('/')[-1]
            return format_html(
                '<a href="{}" target="_blank">' +
                '<img src="https://img.youtube.com/vi/{}/0.jpg" style="height: 50px;" />' +
                '</a>',
                obj.youtube_url,
                video_id
            )
        return "No Video"
    youtube_preview.short_description = 'Video Preview'
    youtube_preview.allow_tags = True

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('question_short', 'lesson', 'type', 'order')
    list_filter = ('type', 'lesson__level')
    search_fields = ('question', 'answer')
    list_select_related = ('lesson',)
    
    def question_short(self, obj):
        return obj.question[:50] + '...' if obj.question else ''
    question_short.short_description = 'Question'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'score', 'completed', 'created')
    list_filter = ('completed', 'lesson__level')
    search_fields = ('user__username', 'lesson__title')
    readonly_fields = ('created',)
    date_hierarchy = 'created'


class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1
    fields = ('front', 'back', 'example', 'difficulty', 'order')


@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'card_count', 'is_public', 'created_at')
    list_filter = ('level', 'is_public')
    search_fields = ('name', 'description')
    inlines = [FlashcardInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'deck', 'difficulty', 'created_at')
    list_filter = ('deck', 'difficulty')
    search_fields = ('front', 'back', 'example')
    readonly_fields = ('created_at', 'updated_at')


class UserFlashcardProgressInline(admin.TabularInline):
    model = UserFlashcardProgress
    extra = 0
    readonly_fields = ('flashcard', 'next_review', 'review_count', 'ease_factor', 'interval', 'created_at', 'updated_at')
    can_delete = False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'streak_days', 'daily_goal', 'last_active')
    list_filter = ('streak_days', 'daily_goal')
    search_fields = ('user__username', 'user__email')
    inlines = [UserFlashcardProgressInline]
    readonly_fields = ('last_active', 'streak_days')
    
    def get_inline_instances(self, request, obj=None):
        # Only show the inlines when editing an existing object
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


class AchievementUserInline(admin.TabularInline):
    model = Achievement.users.through
    extra = 1
    verbose_name = 'User with this achievement'
    verbose_name_plural = 'Users with this achievement'


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'user_count', 'icon_display')
    list_filter = ('points_required',)
    search_fields = ('name', 'description')
    inlines = [AchievementUserInline]
    exclude = ('users',)
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'
    
    def icon_display(self, obj):
        return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
    icon_display.short_description = 'Icon Preview'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('author', 'created_at', 'updated_at')


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'author', 'is_pinned', 'is_closed', 'created_at')
    list_filter = ('is_pinned', 'is_closed', 'lesson__level')
    search_fields = ('title', 'content', 'author__username')
    inlines = [CommentInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'discussion', 'author', 'is_answer', 'created_at')
    list_filter = ('is_answer', 'created_at')
    search_fields = ('content', 'author__username', 'discussion__title')
    readonly_fields = ('created_at', 'updated_at')
    
    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Content'
