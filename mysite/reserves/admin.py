from django.contrib import admin
from .models import Store,Staff,Booking,DefaultValue,MaxNum


admin.site.register(Store)#adminでmodels.pyに追加したStoreクラスを編集できるようにする設定
admin.site.register(Staff)#adminでmodels.pyに追加したStaffクラスを編集できるようにする設定
admin.site.register(Booking)#adminでmodels.pyに追加したBookingクラスを編集できるようにする設定
admin.site.register(DefaultValue)#adminでmodels.pyに追加したBookingクラスを編集できるようにする設定
admin.site.register(MaxNum)#adminでmodels.pyに追加したBookingクラスを編集できるようにする設定