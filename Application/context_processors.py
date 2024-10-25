def selected_language(request):
    selected_language = request.session.get('selected_language', 'default_language')
    return {'selected_language': selected_language}