new Vue({
    el: '#app',
    data: {
        filters: {
            patient_name: '',
            doctor_name: ''
        },
        appointments: []
    },
    methods: {
        submitForm() {
            console.log('Form submitted with filters:', this.filters); // 確認輸入框的值
            this.fetchAppointments();
        },
        async fetchAppointments() {
            try {
                // 打印篩選條件
                console.log(`Filtering by patient_name: ${this.filters.patient_name}, doctor_name: ${this.filters.doctor_name}`);
                console.log('Filters before API call:', this.filters); // 檢查 filters 的值

                // 發送 API 請求，並將 filters 傳入參數
                const response = await axios.get('/appointments/api/appointments/', {
                    params: this.filters
                });

                // 更新篩選結果
                this.appointments = response.data;

            } catch (error) {
                console.error('Error fetching appointments:', error);
                alert('Failed to fetch appointments. Please try again.');
            }
        },
        updateValue(appointmentId, newValue) {
            const checkbox = document.getElementById(`update_${appointmentId}`);
            if (checkbox) {
                checkbox.value = `${appointmentId}:${newValue}`;
            }
        }
    },
    created() {
        // 頁面加載時預先載入所有掛號
        this.fetchAppointments();
    }
});
