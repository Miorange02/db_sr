new Vue({
    el: '#app',
    delimiters: ['${', '}$'],
    data: {
        characters: [],
        page: 1,
        per_page: 9,
        total: 0
    },
    computed: {
        totalPages() {
            return Math.ceil(this.total / this.per_page);
        }
    },
    methods: {
        fetchCharacters(page = 1) {
            axios.get('/equipments', {
                params: {page: page, per_page: this.per_page}
            })
                .then(response => {
                    this.characters = response.data.data;
                    this.total = response.data.total;
                    this.page = page;
                })
                .catch(error => {
                    console.error('Error loading characters:', error);
                });
        },
        changePage(p) {
            if (p >= 1 && p <= this.totalPages) {
                this.fetchCharacters(p);
            }
        },
        changeWeapon(characterId) {
            const payload = {
                weapon_id: prompt("请输入要更换的光锥ID:")
            };

            axios.post(`/equipments/${characterId}`, payload)
                .then(response => {
                    alert(response.data.message);
                    this.fetchCharacters(this.page);
                })
                .catch(error => {
                    const status = error.response?.status;
                    let message = "服务器连接异常，请检查网络后重试";

                    if (status === 404) message = "角色不存在";
                    if (status === 400) message = "光锥不存在或参数错误";
                    if (status === 500) message = "服务器内部错误";

                    alert(`操作失败: ${message}`);
                });
        }

    },
    mounted() {
        this.fetchCharacters();
    }
});