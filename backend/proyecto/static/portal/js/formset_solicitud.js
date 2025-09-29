document.addEventListener('DOMContentLoaded', function () {

    function updateFormIndices() {
        const forms = document.querySelectorAll('#documentos-forms .formset-form');
        forms.forEach((form, i) => {
            const input = form.querySelector('input[type="file"]');
            if (input) {
                input.name = `documentos-${i}-archivo`;
                input.id = `id_documentos-${i}-archivo`;
            }
            const deleteCheckbox = form.querySelector('input[type="checkbox"]');
            if (deleteCheckbox) {
                deleteCheckbox.name = `documentos-${i}-DELETE`;
            }
        });
        const totalFormsInput = document.querySelector('#documentos-fieldset input[name$="TOTAL_FORMS"]');
        if (totalFormsInput) totalFormsInput.value = forms.length;
    }

    window.removeForm = function (element) {
        const formDiv = element.closest('.formset-form');
        formDiv.remove();
        updateFormIndices();
    };

    document.getElementById('add-documento').addEventListener('click', function () {
        const container = document.getElementById('documentos-forms');
        const maxForms = parseInt(document.getElementById('documentos-fieldset').dataset.max);
        const currentForms = container.querySelectorAll('.formset-form').length;
        if (currentForms >= maxForms) return;
        const template = document.getElementById('documentos-empty-form').innerHTML.replace(/__prefix__/g, currentForms);
        container.insertAdjacentHTML('beforeend', template);
        updateFormIndices();
    });
});
