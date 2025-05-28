new Vue({
    el: '#app',
    delimiters: ['${', '}$'],
    data: {
        formData: {
            name: '',
            path: '',
            bonus_hp: 1000
        },
        isLoading: false,
        errorMessage: ''
    },
    methods: {
        submitForm() {
            this.isLoading = true;
            this.errorMessage = '';
            axios.post('/weapons/add', this.formData)
                .then(response => {
                    if (response.data.status === 'success') {
                        alert('光锥添加成功,ID=' + response.data.id);
                        window.location.href = '/weapons';
                    } else {
                        this.errorMessage = response.data.message || '添加失败';
                    }
                })
                .catch(error => {
                    this.errorMessage = error.response?.data?.message ||
                        error.message ||
                        '请求失败，请稍后重试';
                    console.error('添加武器错误:', error);
                })
                .finally(() => {
                    this.isLoading = false;
                });
        }
    }
});
