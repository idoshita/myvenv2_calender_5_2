from django.urls import path
from reserves import views

urlpatterns = [
    path("store",views.StoreView.as_view(),name="reserves_store"),
    path("staff/<int:pk>",views.StaffView.as_view(),name="reserves_staff"),
    path("calendar/<int:pk>",views.CalendarView.as_view(),name="reserves_calendar"),#calendarのURLで日程を指定しない場合のURL
    path("calendar/<int:pk>/<int:year>/<int:month>/<int:day>",views.CalendarView.as_view(),name="reserves_calendar"),#calendarのURLで日程を指定する場合のURL
    path("booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>",views.BookingView.as_view(),name="reserves_booking"),#calendarをクリックすると予約ができる機能のURL
    path("thanks",views.ThanksView.as_view(),name="reserves_thanks"),#予約完了画面のサンクスビュー
    # path("mypage/<int:pk>/<int:year>/<int:month>/<int:day>",views.MypageView.as_view(),name="reserves_mypage"),#スタッフが予約を確認できるURL
    path("mypage/<int:year>/<int:month>/<int:day>",views.MypageView.as_view(),name="reserves_mypage"),#スタッフが予約を確認できるURL
    path("mypage/holiday/<int:year>/<int:month>/<int:day>/<int:hour>",views.Holiday,name="reserves_holiday"),#スタッフが休日を設定できるURL
    path("mypage/delete/<int:year>/<int:month>/<int:day>/<int:hour>",views.Delete,name="reserves_delete"),#スタッフが休日を設定できるURL
    path("toreserves/<int:year>/<int:month>/<int:day>/<int:hour>",views.Toreserves.as_view(),name="reserves_toreserves"),#スタッフが日時予約を確認できるURL
    path("numchange",views.NumChange.as_view(),name="reserves_numchange"),#スタッフが各日時の最大予約数を設定できるURL
    path("numchange/<int:year>/<int:month>/<int:day>",views.NumChange.as_view(),name="reserves_numchange"),#スタッフが各日時の最大予約数を設定できるURL
    path("mypage/holidayall/<int:year>/<int:month>/<int:day>",views.HolidayAll,name="reserves_holidayall"),#スタッフが終日休日を設定できるURL

]
