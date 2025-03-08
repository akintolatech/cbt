from .models import AppInfo


def app_information(request):
    # Fetch the first WebDetails object (you can customize the query if necessary)
    app_info = AppInfo.objects.first()

    return {
        'app_info': app_info
    }