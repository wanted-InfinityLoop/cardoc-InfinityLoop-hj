import json

from django.db            import transaction
from django.http          import JsonResponse
from django.forms.models import model_to_dict 
from django.views.generic import View

from users.models   import User
from cars.models    import Car, FrontTire, RearTire, Spec
from core.utils     import login_check, get_car_info, create_tire


class CarView(View):
    @login_check
    def get(self, request):
        try:
            user_id = request.GET.get("id")

            if request.user.id != user_id:
                return JsonResponse({"message":"WRONG USER"}, status=401)

            f_dict = model_to_dict(
                User.objects.get(id=request.user.id).car.spec.front_tire, 
                                fields=["name", "width", "aspect_ratio", "wheel_size"]
                )   
            
            r_dict = model_to_dict(
                User.objects.get(id=request.user.id).car.spec.rear_tire, 
                                fields=["name", "width", "aspect_ratio", "wheel_size"]
                )
            
        except AttributeError:
            return JsonResponse({"message":"NOT FOUND TIRE INFO"}, status=404)

        return JsonResponse({f"{request.user.id} TIRE INFORMATION": [f_dict, r_dict]}, status=200)


    def post(self, request):
        saved_tire_list   = []
        unsaved_tire_list = []
        
        datas = json.loads(request.body)
        
        if len(datas) > 5:
            return JsonResponse({'message': "THE MAXIMUM NUMBER OF TIRES STORED IS 5"}, status=400)

        for data in datas:
            try:
                info = get_car_info(data)

                if not Car.objects.filter(name=info["car_name"]).exists():
                
                    with transaction.atomic():
                        car = Car.objects.create(
                            name     =info["car_name"], 
                            brand    =info["car_brand"], 
                            year_type=info["year_type"]
                            )
                        
                        f_tire = create_tire(FrontTire, info["car_name"], info["front_tire"])
                        r_tire = create_tire(RearTire, info["car_name"], info["rear_tire"])

                        Spec.objects.create(
                            car       =car,
                            front_tire=f_tire,
                            rear_tire =r_tire
                            )

                else:
                    car = Car.objects.get(name=info["car_name"])
                
                user     = User.objects.get(id=data["id"])
                user.car = car
                user.save()

                saved_tire_list.append(data["id"])

            except KeyError:
                return JsonResponse({'message': "KEY ERROR"}, status=400)
            
            except:
                unsaved_tire_list.append(data["id"])

        return JsonResponse({
            "USER TIRE SAVED"  : sorted(list(set(saved_tire_list))),
            "USER TIRE UNSAVED": sorted(list(set(unsaved_tire_list)))
            },
            status=200
        )
