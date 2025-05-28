new Vue({
    el: '#app',
    delimiters: ['${', '}$'],
    data: {
        weapons: [],
        searchId: '',
        searchName: '',
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
        fetchWeapons(page = 1) {
            axios.get('/weapons/', {
                params: {page: page, per_page: this.per_page}
            })
                .then(response => {
                    this.weapons = response.data.data || [];
                    this.total = response.data.total || 0;
                    this.page = page;
                });
        },
        searchWeapons(page = 1) {
            axios.get('/weapons/search', {
                params: {
                    id: this.searchId,
                    name: this.searchName,
                    page: page,
                    per_page: this.per_page
                }
            })
                .then(response => {
                    this.weapons = response.data.data || [];
                    this.total = response.data.total || 0;
                    this.page = response.data.page || 1;
                });
        },
        editWeapon(weapon) {
            // 创建模态框DOM
            const modal = document.createElement('div');
            modal.innerHTML = `
            <div class="modal fade" id="editWeaponModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">编辑武器</h5>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">武器名称</label>
                                <input type="text" class="form-control" id="editWeaponName" value="${weapon.name}" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">命途</label>
                                <select class="form-select" id="editWeaponPath" required>
                                    <option value="毁灭" ${weapon.path === '毁灭' ? 'selected' : ''}>毁灭</option>
                                    <option value="巡猎" ${weapon.path === '巡猎' ? 'selected' : ''}>巡猎</option>
                                    <option value="智识" ${weapon.path === '智识' ? 'selected' : ''}>智识</option>
                                    <option value="同谐" ${weapon.path === '同谐' ? 'selected' : ''}>同谐</option>
                                    <option value="丰饶" ${weapon.path === '丰饶' ? 'selected' : ''}>丰饶</option>
                                    <option value="存护" ${weapon.path === '存护' ? 'selected' : ''}>存护</option>
                                    <option value="虚无" ${weapon.path === '虚无' ? 'selected' : ''}>虚无</option>
                                    <option value="记忆" ${weapon.path === '记忆' ? 'selected' : ''}>记忆</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">生命值加成</label>
                                <input type="number" class="form-control" id="editWeaponBonusHp" value="${weapon.bonus_hp}" min="1" required>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                            <button type="button" class="btn btn-primary" id="confirmEditWeapon">保存</button>
                        </div>
                    </div>
                </div>
            </div>`;

            document.body.appendChild(modal);

            // 初始化Bootstrap模态框
            const modalInstance = new bootstrap.Modal(modal.querySelector('.modal'));
            modalInstance.show();

            // 确认按钮事件
            modal.querySelector('#confirmEditWeapon').addEventListener('click', () => {
                const name = modal.querySelector('#editWeaponName').value.trim();
                const path = modal.querySelector('#editWeaponPath').value;
                const bonus_hp = Number(modal.querySelector('#editWeaponBonusHp').value);

                if (!name || !path || isNaN(bonus_hp) || bonus_hp <= 0) {
                    alert('请填写完整且有效的表单数据');
                    return;
                }

                axios.put(`/weapons/${weapon.id}`, {
                    name,
                    path,
                    bonus_hp
                })
                    .then(response => {
                        modalInstance.hide();
                        modal.remove();
                        if (response.data.success) {
                            this.fetchWeapons(this.page);
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
        deleteWeapon(id) {
            if (!confirm('确定要删除该武器吗？')) return;
            axios.delete(`/weapons/${id}`)
                .then(response => {
                    if (response.data.status === 'success') {
                        this.fetchWeapons(this.page);
                    } else {
                        alert(response.data.message || '删除失败');
                    }
                });
        },
        changePage(p) {
            if (p < 1 || p > this.totalPages) return;
            this.fetchWeapons(p);
        }
    },
    mounted() {
        this.fetchWeapons();
    }
});
