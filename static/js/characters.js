new Vue({
    el: '#app',
    delimiters: ['${', '}$'],
    data: {
        characters: [],
        searchId: '',
        searchName: '',
        newCharacter: {
            name: '',
            path: '',
            base_hp: 1000,
            profile: ''
        },
        page: 1,
        per_page: 10,
        total: 0
    },
    computed: {
        totalPages() {
            return Math.max(1, Math.ceil(this.total / this.per_page));
        }
    },
    methods: {
        fetchCharacters(page = 1) {
            axios.get('/characters/', {
                params: {page: page, per_page: this.per_page}
            })
                .then(response => {
                    this.characters = response.data.data || [];
                    this.total = response.data.total || 0;
                    this.page = page;
                });
        },
        searchCharacters(page = 1) {
            axios.get('/characters/search', {
                params: {
                    id: this.searchId,
                    name: this.searchName,
                    page: page,
                    per_page: this.per_page
                }
            })
                .then(response => {
                    this.characters = response.data.data || [];
                    this.total = response.data.total || 0;
                    this.page = response.data.page || 1;
                });
        },
        editCharacter(character) {
            // 创建模态框DOM
            console.log(character);
            const modal = document.createElement('div');
            modal.innerHTML = `
    <div class="modal fade" id="editModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">编辑角色</h5>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">角色名称</label>
                        <input type="text" class="form-control" id="editName" value="${character.name}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">命途</label>
                        <select class="form-select" id="editPath" required>
                            <option value="毁灭" ${character.path === '毁灭' ? 'selected' : ''}>毁灭</option>
                            <option value="巡猎" ${character.path === '巡猎' ? 'selected' : ''}>巡猎</option>
                            <option value="智识" ${character.path === '智识' ? 'selected' : ''}>智识</option>
                            <option value="同谐" ${character.path === '同谐' ? 'selected' : ''}>同谐</option>
                            <option value="丰饶" ${character.path === '丰饶' ? 'selected' : ''}>丰饶</option>
                            <option value="存护" ${character.path === '存护' ? 'selected' : ''}>存护</option>
                            <option value="虚无" ${character.path === '虚无' ? 'selected' : ''}>虚无</option>
                            <option value="记忆" ${character.path === '记忆' ? 'selected' : ''}>记忆</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">基础生命值</label>
                        <input type="number" class="form-control" id="editHp" value="${character.base_hp}" min="1" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">角色介绍</label>
                        <textarea class="form-control" id="editProfile">${character.profile}</textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" id="confirmEdit">保存</button>
                </div>
            </div>
        </div>
    </div>`;

            document.body.appendChild(modal);

            // 初始化Bootstrap模态框
            const modalInstance = new bootstrap.Modal(modal.querySelector('.modal'));
            modalInstance.show();

            // 确认按钮事件
            modal.querySelector('#confirmEdit').addEventListener('click', () => {
                const name = modal.querySelector('#editName').value.trim();
                const path = modal.querySelector('#editPath').value;
                const hp = Number(modal.querySelector('#editHp').value);
                const profile = modal.querySelector('#editProfile').value.trim();

                if (!name || !path || isNaN(hp) || hp <= 0) {
                    alert('请填写完整且有效的表单数据');
                    return;
                }

                axios.put(`/characters/${character.id}`, {
                    name,
                    path,
                    base_hp: hp,
                    profile
                })
                    .then(response => {
                        modalInstance.hide();
                        modal.remove();
                        if (response.data.success) {
                            this.fetchCharacters(this.page);
                        }
                    })
                    .catch(error => {
                        alert(`保存失败: ${error.response?.data?.message || error.message}`);
                    });
            });

            // 模态框关闭时清理
            modal.querySelector('.modal').addEventListener('hidden.bs.modal', () => {
                modal.remove();
            });
        },

        deleteCharacter(id) {
            if (confirm('确定要删除该角色吗？')) {
                axios.delete(`/characters/${id}`)
                    .then(response => {
                        if (response.data.status === 'success') {
                            // 如果当前页数据被删空，自动跳到上一页
                            if (this.characters.length === 1 && this.page > 1) {
                                this.fetchCharacters(this.page - 1);
                            } else {
                                this.fetchCharacters(this.page);
                            }
                        } else {
                            alert(response.data.message);
                        }
                    });
            }
        },
        changePage(p) {
            if (p >= 1 && p <= this.totalPages) {
                // 判断是否在搜索
                if (this.searchId || this.searchName) {
                    this.searchCharacters(p);
                } else {
                    this.fetchCharacters(p);
                }
            }
        }
    },
    mounted() {
        this.fetchCharacters();
    }
});
