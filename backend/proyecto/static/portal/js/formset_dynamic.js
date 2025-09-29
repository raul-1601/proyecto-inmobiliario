document.addEventListener('DOMContentLoaded', function () {

    function updateFormIndices(fieldsetId, prefix) {
        const forms = document.querySelectorAll(`#${fieldsetId} .formset-form`);
        forms.forEach((form, i) => {
            const input = form.querySelector('input[type="file"]');
            if (input) {
                input.name = `${prefix}-${i}-${input.name.split('-').pop()}`;
                input.id = `id_${prefix}-${i}-${input.id.split('-').pop()}`;
            }
        });
        const totalFormsInput = document.querySelector(`#${fieldsetId} input[name$="TOTAL_FORMS"]`);
        if (totalFormsInput) totalFormsInput.value = forms.length;
    }

    window.removeForm = function (element) {
        const formDiv = element.closest('.formset-form');
        const fieldset = formDiv.closest('fieldset');
        formDiv.remove();
        if (fieldset.id === 'imagenes-fieldset') {
            updateFormIndices('imagenes-fieldset', 'imagenes');
        } else if (fieldset.id === 'documentos-fieldset') {
            updateFormIndices('documentos-fieldset', 'documentos');
        }
    };

    document.getElementById('add-imagen').addEventListener('click', function () {
        const container = document.getElementById('imagenes-forms');
        const maxForms = parseInt(document.getElementById('imagenes-fieldset').dataset.max);
        const currentForms = container.querySelectorAll('.formset-form').length;
        if (currentForms >= maxForms) return;
        const totalFormsInput = document.querySelector('#imagenes-fieldset input[name$="TOTAL_FORMS"]');
        const index = currentForms;
        const template = document.getElementById('imagenes-empty-form').innerHTML.replace(/__prefix__/g, index);
        container.insertAdjacentHTML('beforeend', template);
        updateFormIndices('imagenes-fieldset', 'imagenes');
    });

    document.getElementById('add-documento').addEventListener('click', function () {
        const container = document.getElementById('documentos-forms');
        const maxForms = parseInt(document.getElementById('documentos-fieldset').dataset.max);
        const currentForms = container.querySelectorAll('.formset-form').length;
        if (currentForms >= maxForms) return;
        const totalFormsInput = document.querySelector('#documentos-fieldset input[name$="TOTAL_FORMS"]');
        const index = currentForms;
        const template = document.getElementById('documentos-empty-form').innerHTML.replace(/__prefix__/g, index);
        container.insertAdjacentHTML('beforeend', template);
        updateFormIndices('documentos-fieldset', 'documentos');
    });

});