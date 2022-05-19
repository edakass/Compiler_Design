import basic
#basic classından  bilgileri kullanmak için gerekli olan kısım,içe aktarıyoruz

#Bu dosya, terminal penceresinden ham girdiyi okuyacak sonsuz bir döngüye sahip olacak.
while True:
    text = input('test > ')

    result, error = basic.run('<stdin>', text)
    
    print(result)

    if error: print(error.as_string())

    elif result: print(result)