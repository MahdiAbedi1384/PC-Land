from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from iranian_cities.models import City, Province
from phonenumber_field.formfields import PhoneNumberField

from .models import Addresses, CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=True)
    phone_number = PhoneNumberField(
        region=settings.PHONENUMBER_DEFAULT_REGION, required=True
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "gender",
            "phone_number",
            "password1",
            "password2",
        )
        exclude = ["username"]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
        # fields = ('username', 'email', 'phone_number')


class CompleteProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=False)
    nat_code = forms.CharField(max_length=10, required=False)
    gender = forms.ChoiceField(choices=[("M", "مرد"), ("F", "زن")], required=True)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = [
            "full_name",
            "phone_number",
            "province",
            "city",
            "full_address",
            "postal_code",
            "is_default",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "province": forms.Select(
                attrs={"class": "form-control", "id": "id_province"}
            ),
            "city": forms.Select(attrs={"class": "form-control", "id": "id_city"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # استان‌ها همیشه باید نمایش داده شوند
        self.fields["province"].queryset = Province.objects.all()

        # اگر province انتخاب شده (در POST)
        if "province" in self.data:
            try:
                province_id = int(self.data.get("province"))
                self.fields["city"].queryset = City.objects.filter(
                    province_id=province_id
                )
            except:
                self.fields["city"].queryset = City.objects.none()

        # اگر فرم در حالت ویرایش است
        elif self.instance.pk and self.instance.province:
            self.fields["city"].queryset = City.objects.filter(
                province=self.instance.province
            )

        # حالت افزودن و province انتخاب‌نشده
        else:
            self.fields["city"].queryset = City.objects.none()
