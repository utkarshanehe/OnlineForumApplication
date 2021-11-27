from online_forum.models import Post


def search(request):
    search_context = {}
    posts = Post.objects.all()

    if "search-form" in request.GET:
        search_query = request.GET.get("search-query")
        search_result = posts.filter(title__icontains=search_query)
        search_context = {
            "search_result": search_result,
            "search_query": search_query,
        }
    return search_context
