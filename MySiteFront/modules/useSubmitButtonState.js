import { computed } from "vue";

export default function useSubmitButtonState(user, errors) {

    // const isSignupButtonDisabled = computed(() => {
    //     let disabled = true;
    //     let checkErrors = false;
    //     let checkEquality = false;


    //     for (let prop in user) {
    //         if (!user[prop] || errors[prop]) {
    //             disabled = true;
    //             break;
    //         }

    //         // disabled = false
    //         checkErrors = true;
    //     }

    //     if ('repeatPassword' in user) {
    //         if (user.password == user.repeatPassword && user.password.length != 0 && user.repeatPassword.length != 0) {
    //             checkEquality = true;
    //         } 
    //     } else {
    //         checkEquality = true;
    //     }


    //     if( checkErrors && checkEquality) {
    //         disabled = false;
    //     }

    //     return disabled
    // });

    const isSignupButtonDisabled = computed(() => {
        // Проверяем, все ли поля формы заполнены
        const allFieldsFilled = Object.keys(user).every((prop) => {
          return user[prop] && !errors[prop]; // Поле должно быть заполнено и без ошибки
        });
    
        // Проверяем совпадение паролей
        const passwordsMatch = 
          'repeatPassword' in user 
          ? user.password === user.repeatPassword && user.password.length > 0
          : true; // Если поле repeatPassword есть, проверяем совпадение, иначе - пропускаем
    
        // Кнопка активна только если все поля заполнены и пароли совпадают
        return !(allFieldsFilled && passwordsMatch);
      });

    return { isSignupButtonDisabled }
}