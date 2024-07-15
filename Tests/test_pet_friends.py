from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Покапика', animal_type='кошка', age='2', pet_photo='images/kot-koshka.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("No pets to delete")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in [pet['id'] for pet in my_pets['pets']]

def test_successful_update_self_pet_info(name='Покапика', animal_type='кошка-двортерьер', age=10):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("No pets to update")

    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_empty_name(animal_type='кошка', age='2', pet_photo='images/kot-koshka.jpg'):
    """Проверяем что нельзя добавить питомца с пустым именем"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, '', animal_type, age, pet_photo)
    assert status != 200

def test_add_new_pet_with_long_name(name='Покапика' * 100, animal_type='кошка', age='2', pet_photo='images/kot-koshka.jpg'):
    """Проверяем что нельзя добавить питомца с очень длинным именем"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200

def test_add_new_pet_with_invalid_animal_type(name='Герда', animal_type='12345', age='4', pet_photo='images/doggy.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным типом животного"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200

def test_add_new_pet_with_invalid_age(name='Герда', animal_type='красавица', age='invalid_age', pet_photo='images/doggy.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным возрастом"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200

def test_add_new_pet_without_photo(name='Герда', animal_type='красавица', age='4'):
    """Проверяем что нельзя добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, '')
    assert status != 200