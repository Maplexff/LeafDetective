import request from '@/utils/request'

// 查询history列表
export function listHistory(query) {
  return request({
    url: '/history/history/list',
    method: 'get',
    params: query
  })
}

// 查询history详细
export function getHistory(id) {
  return request({
    url: '/history/history/getById/' + id,
    method: 'get'
  })
}

// 新增history
export function addHistory(data) {
  return request({
    url: '/history/history/add',
    method: 'post',
    data: data
  })
}

// 修改history
export function updateHistory(data) {
  return request({
    url: '/history/history/update',
    method: 'put',
    data: data
  })
}

// 删除history
export function delHistory(id) {
  return request({
    url: '/history/history/delete/' + id,
    method: 'delete'
  })
}

// 导入history
export function importHistory(data) {
    return request({
      url: '/history/history/import',
      method: 'post',
      data: data
    })
}