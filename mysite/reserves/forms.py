from django import forms


class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="姓")
    last_name = forms.CharField(max_length=100, label="名")
    tel = forms.CharField(max_length=100, label="電話番号")
    adlutnum = forms.IntegerField(label="大人人数")
    childnum = forms.IntegerField(label="子供人数")



class MaxNumForm(forms.Form):
    maxnum = forms.IntegerField(label="予約最大数")


class MaxNumeForm(forms.Form):
    maxnum = forms.IntegerField(label="予約最大数")


class DefaultValueForm(forms.Form):
    defaultvalue = forms.IntegerField(label="全日予約数")
