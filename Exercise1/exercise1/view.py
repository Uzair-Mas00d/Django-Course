from django.http import HttpResponse

def index(request):
    s = '''<h1>Navigation Bar</h1>
        <a href="https://www.djangoproject.com/">DJANGO</a><br>
        <a href="https://www.facebook.com/campaign/landing.php?campaign_id=1653377901&extra_1=s%7Cc%7C318307045126%7Ce%7Cfacebook%27%7C&placement=&creative=318307045126&keyword=facebook%27&partner_id=googlesem&extra_2=campaignid%3D1653377901%26adgroupid%3D65139789042%26matchtype%3De%26network%3Dg%26source%3Dnotmobile%26search_or_content%3Ds%26device%3Dc%26devicemodel%3D%26adposition%3D%26target%3D%26targetid%3Dkwd-362360550869%26loc_physical_ms%3D1011077%26loc_interest_ms%3D%26feeditemid%3D%26param1%3D%26param2%3D&gclid=Cj0KCQjw27mhBhC9ARIsAIFsETEpWE2QHzndLJqkXaDD8NKUlUM2zU6Uy79Rm-49f1Yb3VwqV5K2KucaAr-kEALw_wcB">FACEBOOK</a><br>
        <a href="https://www.youtube.com/">YOUTUBE</a><br>
        <a href="https://www.google.com/">GOOGLE</a><br>
        <a href="https://www.instagram.com/">INSTAGRAM</a><br>
    '''
    return HttpResponse(s)