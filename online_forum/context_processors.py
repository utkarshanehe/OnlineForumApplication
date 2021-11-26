from online_forum.models import Post


def search(request):
    search_context = {}
    posts = Post.objects.all()

    if "search-form" in request.GET:
        search_query = request.GET.get("search-query")

        # Filter starts here
        search_box = request.GET.get("search-box")
        if search_box == "Descriptions":
            search_result = posts.filter(content__icontains=search_query)
        else:
            search_result = posts.filter(title__icontains=search_query)
        # Ends here

        search_context = {
            "search_result": search_result,
            "search_query": search_query,
        }
    return search_context
