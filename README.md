# chat-app
 fullstack chat app(django+react)

Bazı fonksiyonların açıklaması:

self.queryset.annotate(num_members=Count("member")) ifadesi, queryset üzerinde num_members adında bir alan oluşturur. Bu alan, member ilişkisi üzerinden hesaplanır ve annotate işlemi sonucunda queryset'e eklenir. Ancak, bu num_members alanı, veritabanında bir alan olarak fiziksel olarak depolanmaz. Sadece annotate işlemi tarafından hesaplanır ve geçici olarak queryset'e eklenir.
Bu durumda, num_members alanını frontend tarafında kullanılabilir hale getirmek için serializers.SerializerMethodField() kullanılmıştır. num_members = serializers.SerializerMethodField() ifadesi, num_members adında bir SerializerMethodField alanı oluşturur. Bu alan, Serializer sınıfı üzerinde kullanılarak, get_num_members gibi bir yönteme bağlanır. Bu yöntem, num_members alanının değerini döndüren özel bir hesaplama yapar.
Bu şekilde, num_members alanını queryset'ten almadan önce get_num_members yöntemi tarafından hesaplanan değeri kullanarak frontend tarafında kullanılabilir hale getirirsiniz. Bu, annotate ile oluşturulan geçici bir alanın, SerializerMethodField ile kullanılarak Serializer'da istediğimiz şekilde temsil edilmesini sağlar.

SerializerMethodField, serializer sınıfında kullanılarak, modelde tanımlanmış alanlar veya ilişkiler üzerinde hesaplamalar yapmak ve bu hesaplamaları frontend tarafında kullanılabilir hale getirmek için kullanılır. Bu nedenle, SerializerMethodField kullanırken modelde tanımlanmış bir objeye ihtiyaç duyulur.

Özetle, SerializerMethodField kullanmak için modelde tanımlanmış bir objeye ihtiyaç vardır. Bu alan veya ilişki üzerindeki hesaplamaları SerializerMethodField ile yapabilir ve bu hesaplamaları frontend tarafında kullanılabilir hale getirebilirsiniz. Annotate işlemi ise veritabanı sorgularıyla çalışır ve veritabanındaki tablolar veya modeller üzerinde hesaplamalar yapar.

Annotate ile oluşturduğunuz alanla SerializerMethodField ile oluşturduğunuz alanı eşleştirmek için aynı adı vermeniz gerekmektedir.

Eğer annotate ile queryset üzerinde bir alan oluşturduysanız ve aynı adı kullanarak SerializerMethodField ile serializer sınıfında bir alan oluşturduysanız, ikisi arasında bir eşleşme sağlayabilirsiniz.

Örneğin, annotate ile oluşturulan num_members alanını ve SerializerMethodField ile oluşturulan num_members alanını aynı adı kullanarak eşleştirmek için şu şekilde yapabilirsiniz:

class ServerSerializer(serializers.Serializer):
    num_members = serializers.SerializerMethodField()

    def get_num_members(self, obj):
        return obj.num_members
Yukarıdaki örnekte, ServerSerializer adında bir serializer sınıfı tanımlanmıştır. Bu sınıf, num_members adında bir alanı SerializerMethodField ile oluşturur. get_num_members yöntemi, bu alanın değerini obj.num_members olarak döndürür.

Eğer annotate ile oluşturulan num_members alanı da aynı adı kullanıyorsa, serializer, num_members adındaki bu alanı queryset nesnelerindeki ilgili değerle eşleştirir.

Bu şekilde, annotate ile oluşturulan num_members alanını queryset'e ekleyebilir ve aynı adı kullandığınız SerializerMethodField ile bu alanın değerini serializer'da temsil edebilirsiniz.

yani queryset objelerini obj olarak alır

Evet, doğru anladınız. SerializerMethodField kullanırken, queryset nesneleri obj olarak temsil edilir.

get_num_members gibi bir yöntem, SerializerMethodField ile ilişkili alanın değerini elde etmek için kullanılır. Bu yöntemde obj parametresi bulunur ve bu parametre aracılığıyla serializer'a geçirilen queryset nesnesini temsil eder.

Örneğin, aşağıdaki gibi bir kullanımı vardır:

class ServerSerializer(serializers.Serializer):
    num_members = serializers.SerializerMethodField()

    def get_num_members(self, obj):
        # obj, queryset nesnesini temsil eder
        # queryset nesnesi üzerinden gerekli hesaplamaları yapabilirsiniz
        return some_calculation(obj)
Yukarıdaki örnekte, ServerSerializer adında bir serializer sınıfı tanımlanmıştır. Bu sınıf, num_members adında bir alanı SerializerMethodField ile oluşturur. get_num_members yöntemi, obj parametresini alır ve bu parametre aracılığıyla queryset nesnesini temsil eder. Bu yöntemde, obj (queryset nesnesi) üzerinde gerekli hesaplamaları yaparak num_members alanının değerini döndürebilirsiniz.

Bu şekilde, SerializerMethodField ile queryset nesnelerini obj olarak alabilir ve bu nesneler üzerinde istediğiniz işlemleri gerçekleştirebilirsiniz.


   @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)


Bu kod parçası, Category modelinden bir örnek silindiğinde (pre_delete sinyali tetiklendiğinde) ilgili icon dosyasının silinmesini sağlamak için kullanılan bir sinyal dinleyicisini (signal receiver) tanımlar.

@receiver(models.signals.pre_delete, sender="server.Category") satırı, pre_delete sinyali Category modelinden bir örnek silindiğinde tetiklenen bir sinyal dinleyicisi olduğunu belirtir. Yani, Category modelindeki herhangi bir örnek silindiğinde, category_delete_files adlı fonksiyon otomatik olarak çalıştırılır.

category_delete_files fonksiyonu, sender, instance ve **kwargs parametrelerini alır. instance parametresi, silinen Category modeli örneğini temsil eder. Bu fonksiyon, örneğin ._meta.fields kullanarak Category modelinin tüm alanlarına erişir ve bu alanların isimlerini kontrol eder.

Döngü içinde, her bir alanın ismi "icon" ile eşleştiğinde, getattr(instance, field.name) kullanarak ilgili dosya alanına (icon) erişir. Ardından, file değişkeni üzerinden bu dosyaya erişilir ve dosya varsa file.delete(save=False) ifadesi ile silinir. save=False parametresi, dosyanın silinmesi için modelin tekrar kaydedilmesini gerektirmez, çünkü burada yalnızca dosyanın silinmesi amaçlanmaktadır.

Bu sinyal dinleyicisi, Category modelinden herhangi bir örnek silindiğinde ilgili icon dosyasını silmeyi sağlar. Bu, örneğin kategori örneği silindiğinde ilişkili ikon dosyasını temizlemek için kullanışlı olabilir.