new Vue({
    el: '#app',
    delimiters: ['${', '}$'],
    data: {
        formData: {
            name: '',
            path: '',
            base_hp: 1000,
            profile: ''
        },
        isLoading: false,
        errorMessage: ''
    },
    methods: {
        submitForm() {
            this.isLoading = true;
            this.errorMessage = '';

            axios.post('/characters/add', this.formData)
                .then(response => {
                    if (response.data.success) {
                        alert('角色添加成功,ID=' + response.data.id);
                        window.location.href = '/characters';
                    } else {
                        this.errorMessage = response.data.message || '添加失败';
                    }
                })
                .catch(error => {
                    this.errorMessage = error.response?.data?.message ||
                        error.message ||
                        '请求失败，请稍后重试';
                    console.error('添加角色错误:', error);
                })
                .finally(() => {
                    this.isLoading = false;
                });
        }
    }
});
