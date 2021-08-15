from django import template
from django.template.base import linebreak_iter
from projects.models import UserProject, UserProjectEvent
from codeblocks.models import CodeBlock

register = template.Library()


@register.inclusion_tag('projects/templatetags/render_codeblock_readonly.html', takes_context=True)
def render_codeblock_readonly(context, project):
    """
    Render project's codeblock.
    """
    codeblock = project.codeblock
    return {
        'codeblock': codeblock,
        'blocks': codeblock.get_blocks(),
        'source_code': codeblock.source_code,
    }


@register.inclusion_tag('projects/templatetags/render_codeblock.html', takes_context=True)
def render_codeblock(context, user_project):
    """
    Render project's codeblock.
    """
    codeblock = user_project.codeblock
    return {
        'user_project': user_project,
        'codeblock': codeblock,
        'blocks': codeblock.get_blocks(),
        'source_code': codeblock.source_code,
        'completed': user_project.is_complete(),
    }


@register.inclusion_tag('projects/templatetags/render_requirements.html')
def render_requirements(project):
    """
    Render project's requirements.
    """
    return {'requirements': project.requirements}


@register.inclusion_tag('projects/templatetags/render_requirements_form.html', takes_context=True)
def render_requirements_form(context, user_project):
    """
    Render user_project's requirements form to updated progress.
    Requirements form only editable by its owner and the user_project not yet completed.
    """
    is_owner = context.request.user == user_project.user
    return {
        'user_project': user_project,
        'requirements': user_project.requirements,
        'is_owner': is_owner,
        'editable': is_owner and user_project.is_in_progress(),
    }


@register.inclusion_tag('projects/templatetags/render_review_request_form.html', takes_context=True)
def render_review_request_form(context, user_project, form):
    """
    The Review Request form always editable by owner even though the project already completed
    so user can edit project links and note if needed.
    """
    is_owner = context.request.user == user_project.user
    return {
        'user_project': user_project,
        'form': form,
        'is_owner': is_owner,
        'editable': is_owner,
    }


@register.inclusion_tag('projects/templatetags/render_tags.html')
def render_tags(project, color='primary'):
    """
    Render project's tags.
    """
    data = {'tags': []}
    if not project.tags:
        return data
    data['tags'] = project.tags.split(',')
    data['color'] = color
    return data


@register.inclusion_tag('projects/templatetags/render_timeline.html', takes_context=True)
def render_timeline(context, user_project):
    """
    Render project's events timeline.
    """
    events = UserProjectEvent.objects \
        .select_related('user') \
        .filter(user_project=user_project) \
        .order_by('created')

    events_with_template = []
    for event in events:
        events_with_template.append({
            'obj': event,
            'tpl': 'projects/templatetags/timeline/type_{}.html'.format(event.event_type)
        })
    return {
        'user_project': user_project,
        'events': events_with_template,
        'user': context.request.user,
    }


@register.inclusion_tag('projects/templatetags/inprogress_projects.html')
def render_inprogress_projects(project):
    user_projects = UserProject.objects.select_related('user').filter(
        project=project,
        status__in=(UserProject.STATUS_IN_PROGRESS,
                    UserProject.STATUS_PENDING_REVIEW,
                    UserProject.STATUS_INCOMPLETE)
    ).order_by('-created')[:5]
    return {
        'items': user_projects
    }


@register.inclusion_tag('projects/templatetags/completed_projects.html')
def render_completed_projects(project):
    user_projects = UserProject.objects.select_related('user').filter(
        project=project,
        status=UserProject.STATUS_COMPLETE
    )[:5]
    return {
        'items': user_projects
    }
