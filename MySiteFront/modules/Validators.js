export default function useValidators() {
    const isEmpty = (fieldName, fieldValue) => {
        return !fieldValue ? "Это поле обязательное" : "";
    }
    const minLength = (fieldName, fieldValue, min) => {
        return fieldValue.length < min ? `Минимальная длинна должна быть ${min}` : "";
    }
    const isEmail = (fieldName, fieldValue) => {
        let regularExpression = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return !regularExpression.test(fieldValue) ? "Не правильно введена почта" : "";
    }
    return {isEmpty, minLength, isEmail}
}