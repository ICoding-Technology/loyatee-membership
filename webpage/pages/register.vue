<template>
    <div class="register-page">
        <div class="register-container">
            <h1>Enter your<br />mobile number</h1>
            <p class="subtitle">We will send you confirmation code</p>

            <div class="phone-display">
                <span class="country-code">🇰🇭 +855</span>
                <div class="digit-slots">
                    <span v-for="i in 9" :key="i" class="digit-slot">
                        <span class="digit">{{ phoneNumber[i - 1] || '' }}</span>
                        <span class="cursor" :class="{ active: phoneNumber.length === i - 1 }"></span>
                    </span>
                </div>
            </div>

            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

            <NumPad @input="handleNumInput" @delete="handleDelete" />

            <button type="button" @click="handleNext" class="btn-next" :disabled="!isValid">
                Get OTP Verification
            </button>

            <p class="terms-text">
                By creating passcode you agree with our<br />
                <a href="#">Terms & Conditions</a> and <a href="#">Privacy Policy</a>
            </p>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    data() {
        return {
            phoneNumber: '',
            errorMessage: ''
        }
    },
    computed: {
        formattedPhoneNumber(): string {
            if (this.phoneNumber.length === 0) {
                return ''
            }
            // Format: XXX XX XX
            const digits = this.phoneNumber.split('')
            const formatted = []
            for (let i = 0; i < digits.length; i++) {
                formatted.push(digits[i])
                if (i === 2 || i === 4) {
                    formatted.push(' ')
                }
            }
            return formatted.join('')
        },
        isValid(): boolean {
            return this.phoneNumber.length >= 8
        }
    },
    methods: {
        handleNumInput(value: string) {
            // Check if first digit is 0
            if (this.phoneNumber.length === 0 && value === '0') {
                this.errorMessage = 'Phone number cannot start with 0'
                setTimeout(() => {
                    this.errorMessage = ''
                }, 3000)
                return
            }

            if (this.phoneNumber.length < 9) {
                this.phoneNumber += value
                this.errorMessage = ''
            }
        },
        handleDelete() {
            if (this.phoneNumber.length > 0) {
                this.phoneNumber = this.phoneNumber.slice(0, -1)
            }
        },
        handleNext() {
            if (this.isValid) {
                console.log('Phone number submitted:', '+855' + this.phoneNumber)
                // Navigate to OTP verification page with phone number
                this.$router.push({
                    path: '/otp-verify',
                    query: { phone: this.phoneNumber }
                })
            }
        }
    }
}
</script>

<style scoped>
.register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    background: #ffffff;
    padding: 20px;
}

.register-container {
    width: 100%;
    max-width: 400px;
    padding: 20px;
}

h1 {
    margin: 0 0 12px 0;
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1.3;
}

.subtitle {
    margin: 0 0 40px 0;
    font-size: 14px;
    color: #999;
}

.phone-display {
    background: transparent;
    padding: 16px 0;
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.country-code {
    color: #999;
    font-size: 16px;
    font-weight: 500;
    flex-shrink: 0;
}

.digit-slots {
    display: flex;
    gap: 4px;
    align-items: center;
    flex: 1;
}

.digit-slot {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 18px;
    flex-shrink: 0;
}

.digit {
    font-size: 16px;
    font-weight: 500;
    color: #1a1a1a;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 18px;
}

.cursor {
    width: 100%;
    height: 2px;
    background: #e0e0e0;
    margin-top: 2px;
    transition: background-color 0.3s;
}

.cursor.active {
    background: #4169E1;
    animation: blink 1s infinite;
}

@keyframes blink {

    0%,
    49% {
        opacity: 1;
    }

    50%,
    100% {
        opacity: 0;
    }
}

.error-message {
    color: #ef4444;
    font-size: 14px;
    text-align: center;
    margin: -30px 0 20px 0;
    min-height: 20px;
}

.btn-next {
    width: 100%;
    padding: 16px;
    background: #4169E1;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
    margin-top: 30px;
}

.btn-next:active:not(:disabled) {
    opacity: 0.8;
}

.btn-next:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.terms-text {
    margin-top: 20px;
    font-size: 12px;
    color: #999;
    text-align: center;
    line-height: 1.5;
}

.terms-text a {
    color: #4169E1;
    text-decoration: none;
}
</style>