<template>
  <div class="bg-white p-4 shadow rounded mb-3">
    <!-- Display mode -->
    <template v-if="!isEditing">
      <h2 class="font-bold">{{ note.title }}</h2>
      <p class="text-sm text-gray-600">{{ note.content }}</p>
      <p class="text-xs text-right">{{ note.created_at }}</p>
      <div class="flex gap-3">
        <button @click="startEditing" class="text-blue-500 text-sm mt-2 cursor-pointer">Edit</button>
        <button @click="$emit('delete', note.id)" class="text-red-500 text-sm mt-2 cursor-pointer">Delete</button>
      </div>
    </template>

    <!-- Edit mode -->
    <template v-else>
      <input
        v-model="editTitle"
        class="font-bold w-full p-1 border rounded mb-2"
        @keydown.enter="saveChanges"
        @keydown.escape="cancelEditing"
      >
      <textarea
        v-model="editContent"
        class="text-sm text-gray-600 w-full p-1 border rounded mb-2"
        rows="3"
        @keydown.ctrl.enter="saveChanges"
        @keydown.escape="cancelEditing"
        ref="contentTextarea"
      ></textarea>
      <p class="text-xs text-right">{{ note.created_at }}</p>
      <div class="flex gap-3">
        <button @click="saveChanges" class="text-green-500 text-sm mt-2 cursor-pointer">
          Save Changes
        </button>
        <button @click="cancelEditing" class="text-gray-500 text-sm mt-2 cursor-pointer">
          Cancel
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const props = defineProps({ note: Object })
const emit = defineEmits(['delete', 'update'])

const isEditing = ref(false)
const editTitle = ref('')
const editContent = ref('')
const contentTextarea = ref(null)
const token = localStorage.getItem('token')

const router = useRouter()

const startEditing = () => {
  isEditing.value = true
  editTitle.value = props.note.title
  editContent.value = props.note.content

  nextTick(() => {
    contentTextarea.value?.focus()
  })
}

const saveChanges = async () => {
  const title = editTitle.value.trim()
  const content = editContent.value.trim()

  if (!title || !content) {
    alert('Title และ Content ห้ามเว้นว่าง')
    return
  }

  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อนทำรายการ')
    return
  }

  const bodyData = { title, content }

  try {
    const response = await axios.put(
      `http://localhost:5000/api/notes/${props.note.id}`, // ✅ ตรวจให้แน่ใจว่า endpoint ตรงกับ backend
      bodyData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    emit('update', response.data)
    isEditing.value = false

    // ✅ Redirect ไปยังหน้า dashboard
    await router.push('/dashboard')
    location.reload() // force reload


  } catch (error) {
    console.error('Error updating note:', error.response?.data || error.message)
    alert('ไม่สามารถอัปเดตบันทึกได้')
  }
}

const cancelEditing = () => {
  isEditing.value = false
}
</script>

