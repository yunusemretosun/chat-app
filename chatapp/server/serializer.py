from rest_framework import serializers

from .models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    # Define a nested serializer field for the associated channels of a Server object
    channel_server = ChannelSerializer(many=True)

    # Define a custom field to include the number of members for each Server object
    num_members = serializers.SerializerMethodField()

    class Meta:
        model = Server
        # Exclude the "member" field from the serialized representation of Server objects
        exclude = [
            "member",
        ]

    def get_num_members(self, obj):
        # Check if the Server object has the "num_members" attribute
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        # Call the parent class's to_representation method to get the default serialized representation
        data = super().to_representation(instance)

        # Retrieve the value of the "with_num_members" key from the context
        with_num_members = self.context.get("with_num_members")

        # If "with_num_members" is False or not provided, remove the "num_members" field from the serialized data
        if not with_num_members:
            data.pop("num_members", None)

        # Return the modified serialized data
        return data


"""
NOTLAR
`ServerSerializer` sinifinizda `channel_server` ve `num_members` adinda iki alan tanimladiginizi ve bu alanlarin UI sayfasinda göründügünü belirtiyorsunuz.

Bu durum, `ServerSerializer` sinifinizdaki alan tanimlamalari ve yapilandirma ile ilgilidir. 

`channel_server = ChannelSerializer(many=True)` ifadesi, `ServerSerializer` sinifinda `channel_server` adinda bir alan olusturdugunu gösterir ve bu alan, `ChannelSerializer` tarafindan seri hale getirilmis verileri icerir. Bu nedenle, `channel_server` alani, `ChannelSerializer`'a dayali olarak otomatik olarak olusturuldu.

`num_members = serializers.SerializerMethodField()` ifadesi, `ServerSerializer` sinifinda `num_members` adinda bir alan tanimladiginizi belirtir. Bu özel bir alandir ve `get_num_members` adinda bir yönteme sahiptir. Bu yöntem, her bir `Server` nesnesi icin `num_members` degerini döndürür.

Daha sonra, `ServerSerializer` sinifinda `to_representation` yöntemini gecersiz kilarsiniz. Bu yöntem, özel bir sekilde seri hale getirme islemi yapmanizi saglar. Bu durumda, `with_num_members` degerine bagli olarak `num_members` alanini serilestirilmis veriden cikarirsiniz.

Sonuc olarak, `ServerSerializer` sinifinizin yapilandirmasi ve `to_representation` yöntemi, `channel_server` ve `num_members` alanlarinin görünür olmasina neden olabilir. Bu nedenle, UI sayfasinda bu alanlarin olustugunu gözlemliyorsunuz.

Özetlemek gerekirse, `ServerSerializer` sinifinizin tanimladigi alanlar ve yapilandirma, `channel_server` ve `num_members` alanlarinin UI sayfasinda görünmesine yol acmaktadir.
"""
"""
Evet, `Meta` sinifi Django REST Framework'te cesitli yerlerde kullanilir ve genellikle benzer islevleri yerine getirir. Bu sinif, bir model tabanli seri hale getirme sinifinin davranisini ve özelliklerini kontrol etmek icin kullanilir.

`Meta` sinifinin kullanimi, `ModelSerializer` sinifi ve onun alt siniflariyla sinirli degildir. Ayni zamanda `ViewSet` siniflarinda, `APIView` siniflarinda, form siniflarinda ve diger Django REST Framework bilesenlerinde de kullanilabilir.

`Meta` sinifi, genellikle asagidaki gibi kullanim senaryolarini icerir:

1. Modelin belirtilmesi: `model` parametresi araciligiyla seri hale getirme isleminin hangi model üzerinde gerceklestirilecegi belirtilir.

2. Alanlarin belirtilmesi: `fields` veya `exclude` parametreleri ile seri hale getirilmesi istenen alanlar veya haric tutulmasi istenen alanlar belirtilebilir.

3. Ek özelliklerin tanimlanmasi: Örnegin, `read_only_fields` veya `extra_kwargs` gibi ek özelliklerin tanimlanmasi icin kullanilabilir.

Yani, `Meta` sinifi, Django REST Framework'te yapilandirma ve davranis kontrolü saglayan bir mekanizmadir. Her kullanimda islevi biraz farkli olabilir, ancak genellikle bir seri hale getirme sinifinin isleyisini ve özelliklerini belirlemek icin kullanilir.
"""
