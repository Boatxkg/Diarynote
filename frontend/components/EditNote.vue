<template>
  <div class="bg-white p-4 shadow rounded mb-3">
    <input v-model="title" class="border" />
    <textarea v-model="content" class="border" />
    <p class="text-xs text-right mt-2">{{ createdAt }}</p>
    <div class="flex gap-3 mt-2">
      <button @click="updateNote" class="text-green-500 text-sm mt-2 cursor-pointer">Save</button>
      <button @click="cancelEdit" class="text-gray-500 text-sm mt-2 cursor-pointer">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const id = route.params.id

const title = ref('')
const content = ref('')
const createdAt = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  title.value = res.data.title
  content.value = res.data.content
  createdAt.value = res.data.created_at
})

const updateNote = async () => {
  if (!title.value.trim()) {
    alert('Title is required')
    return
  }

  const token = localStorage.getItem('token')
  await axios.put(`http://localhost:5000/api/notes/${id}`, {
    title: title.value,
    content: content.value
  }, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  window.location.href = '/dashboard'
}

</script>
