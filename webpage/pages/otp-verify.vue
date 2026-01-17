<template>
    <div class="otp-page">
        <div class="otp-container">
            <h1>Enter OTP<br />verification code</h1>
            <p class="subtitle">We have sent the code to +855 {{ maskedPhone }}</p>

            <div class="otp-display">
                <div class="otp-slots">
                    <span v-for="i in 6" :key="i" class="otp-slot" :class="{ active: otpCode.length === i - 1 }">
                        <span class="digit">{{ otpCode[i - 1] || '' }}</span>
                    </span>
                </div>
            </div>

            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

            <NumPad @input="handleNumInput" @delete="handleDelete" />

            <button type="button" @click="handleVerify" class="btn-verify" :disabled="!isValid">
                Verify OTP
            </button>

            <div class="resend-container">
                <p class="resend-text">
                    Didn't receive the code?
                    <button v-if="canResend" @click="handleResend" class="resend-link" type="button">
                        Resend
                    </button>
                    <span v-else class="resend-timer">Resend in {{ countdown }}s</span>
                </p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    data() {
        return {
            otpCode: '',
            errorMessage: '',
            countdown: 60,
            canResend: false,
            timerInterval: null as number | null
        }
    },
    computed: {
        maskedPhone(): string {
            // Get phone from route query or use placeholder
            const phone = (this.$route.query.phone as string) || '123456789'
            return phone.substring(0, 3) + '***' + phone.substring(6)
        },
        isValid(): boolean {
            return this.otpCode.length === 6
        }
    },
    mounted() {
        this.startCountdown()
    },
    beforeUnmount() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval)
        }
    },
    methods: {
        handleNumInput(value: string) {
            if (this.otpCode.length < 6) {
                this.otpCode += value
                this.errorMessage = ''
            }
        },
        handleDelete() {
            if (this.otpCode.length > 0) {
                this.otpCode = this.otpCode.slice(0, -1)
                this.errorMessage = ''
            }
        },
        handleVerify() {
            if (this.isValid) {
                console.log('OTP submitted:', this.otpCode)
                // Navigate to home page
                this.$router.push('/home')
            }
        },
        handleResend() {
            if (this.canResend) {
                console.log('Resending OTP...')
                // Handle resend OTP logic here
                this.otpCode = ''
                this.errorMessage = ''
                this.countdown = 60
                this.canResend = false
                this.startCountdown()
            }
        },
        startCountdown() {
            if (this.timerInterval) {
                clearInterval(this.timerInterval)
            }
            this.timerInterval = setInterval(() => {
                if (this.countdown > 0) {
                    this.countdown--
                } else {
                    this.canResend = true
                    if (this.timerInterval) {
                        clearInterval(this.timerInterval)
                    }
                }
            }, 1000) as unknown as number
        }
    }
}
</script>

<style scoped>
.otp-page {
    display: flex;
    justify-content: center;
    align-items: center;
    background: #ffffff;
    padding: 20px;
    overflow-y: auto;
}

.otp-container {
    width: 100%;
    max-width: 400px;
    padding: 10px;
}

h1 {
    margin: 0 0 8px 0;
    font-size: 22px;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1.3;
}

.subtitle {
    margin: 0 0 30px 0;
    font-size: 13px;
    color: #999;
}

.otp-display {
    background: transparent;
    padding: 12px 0;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.otp-slots {
    display: flex;
    gap: 6px;
    align-items: center;
}

.otp-slot {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 45px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    background: #ffffff;
    transition: border-color 0.3s;
}

.otp-slot.active {
    border-color: #4169E1;
}

.digit {
    font-size: 20px;
    font-weight: 600;
    color: #1a1a1a;
}

.cursor {
    display: none;
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
    font-size: 13px;
    text-align: center;
    margin: -25px 0 15px 0;
    min-height: 18px;
}

.btn-verify {
    width: 100%;
    padding: 14px;
    background: #4169E1;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
    margin-top: 20px;
}

.btn-verify:active:not(:disabled) {
    opacity: 0.8;
}

.btn-verify:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.resend-container {
    margin-top: 16px;
}

.resend-text {
    font-size: 14px;
    color: #666;
    text-align: center;
    margin: 0;
}

.resend-link {
    background: none;
    border: none;
    color: #4169E1;
    font-weight: 600;
    cursor: pointer;
    padding: 0;
    margin-left: 4px;
    font-size: 14px;
}

.resend-link:active {
    opacity: 0.7;
}

.resend-timer {
    color: #999;
    margin-left: 4px;
    font-weight: 600;
}
</style>
