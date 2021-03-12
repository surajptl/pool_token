from django.urls import path
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('generate-pool-tokens/<int:pool_name>/<int:pool_size>', generate_pool),
    path('get-pool/<int:pool_name>', get_pool),
    path('assign-token/<int:pool_name>', assign_token),
    path('unbloked-token/<token_name>', unblocked_token),
    path('delete-token/<token_name>', delete_token),
    path('keep-alive-token', keep_alive_token),
    path('automatically_freed_or_released', freed_or_released)
]