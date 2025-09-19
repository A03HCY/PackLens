class MIcon extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        // 获取原始内容
        const content = this.innerHTML.trim();

        // 清除现有内容
        this.innerHTML = '';

        // 创建s-icon元素
        const sIcon = document.createElement('s-icon');

        // 创建内部span
        const iconSpan = document.createElement('span');
        iconSpan.className = 'icon';
        iconSpan.innerHTML = content;

        // 组装结构
        sIcon.appendChild(iconSpan);
        this.appendChild(sIcon);
    }
}
customElements.define('m-icon', MIcon);
