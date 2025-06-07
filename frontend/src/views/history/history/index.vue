<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">

            <el-form-item label="图像ID" prop="id">
              <el-input
                v-model="queryParams.id"
                placeholder="请输入图像ID"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>
            <el-form-item label="上报ID" prop="reportid">
              <el-input
                v-model="queryParams.reportid"
                placeholder="请输入上报ID"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>

            <el-form-item label="上报地址" prop="location">
              <el-input
                v-model="queryParams.location"
                placeholder="请输入上报地址"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>
            <!-- <el-form-item label="预测类别" prop="predclass">
              <el-input
                v-model="queryParams.predclass"
                placeholder="请输入预测类别"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item> -->
            <el-form-item label="预测类别" prop="predclass">
              <el-select
                  v-model="queryParams.predclass"
                  placeholder="请选择预测类别"
                  style="width: 180px"
                  clearable>
                <el-option
                  v-for="dict in predclass_type"
                  :key="dict.value"
                  :label="dict.label"
                  :value="dict.value"
                />
              </el-select>
            </el-form-item>

      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-card class="base-table" ref="fullTable">
            <TableSetup
                ref="tSetup"
                @onStripe="onStripe"
                @onRefresh="onRefresh"
                @onChange="onChange"
                @onfullTable="onfullTable"
                @onSearchChange="onSearchChange"
                :columns="columns"
                :isTable="isTable"
            >
                <template v-slot:operate>
                    <el-button
                      type="primary"
                      plain
                      icon="Plus"
                      @click="handleAdd"
                      v-hasPermi="['history:history:add']"
                    >新增</el-button>
                    <el-button
                      type="success"
                      plain
                      icon="Edit"
                      :disabled="single"
                      @click="handleUpdate"
                      v-hasPermi="['history:history:edit']"
                    >修改</el-button>
                    <el-button
                      type="danger"
                      plain
                      icon="Delete"
                      :disabled="multiple"
                      @click="handleDelete"
                      v-hasPermi="['history:history:remove']"
                    >删除</el-button>
                  <el-button
                        type="primary"
                        plain
                        icon="Upload"
                        @click="handleImport"
                        v-hasPermi="['history:history:import']"
                        >导入</el-button
                    >
                    <el-button
                      type="warning"
                      plain
                      icon="Download"
                      @click="handleExport"
                      v-hasPermi="['history:history:export']"
                    >导出</el-button>
                </template>
            </TableSetup>
            <auto-table
                ref="multipleTable"
                class="mytable"
                :tableData="historyList"
                :columns="columns"
                :loading="loading"
                :stripe="stripe"
                :tableHeight="tableHeight"
                @onColumnWidthChange="onColumnWidthChange"
                @onSelectionChange="handleSelectionChange"
            >






                    <template #image="{ row }">
                      <image-preview :src="fullUrl(row.image)"  v-if="row.image" :width="50" :height="50"/>
                    </template>










                    <template #updateTime="{ row }">
                      <span>{{ parseTime(row.updateTime, '{y}-{m}-{d}') }}</span>
                    </template>
                <template #operate="{ row }">
                  <el-button link type="primary" icon="Edit" @click="handleUpdate(row)" v-hasPermi="['history:history:edit']">修改</el-button>
                  <el-button link type="primary" icon="Delete" @click="handleDelete(row)" v-hasPermi="['history:history:remove']">删除</el-button>
                </template>
            </auto-table>
            <div class="table-pagination">
                <pagination
                    v-show="total > 0"
                    :total="total"
                    v-model:page="queryParams.pageNum"
                    v-model:limit="queryParams.pageSize"
                    @pagination="getList"
                />
            </div>
        </el-card>

    <!-- 添加或修改history对话框 -->
    <el-dialog :title="title" v-model="open" width="800px" append-to-body>
      <el-form ref="historyRef" :model="form" :rules="rules" label-width="80px">

                <el-form-item label="图像" prop="image">
                  <image-upload v-model="form.image"/>
                </el-form-item>

                <el-form-item label="纬度" prop="lat">
                  <el-input v-model="form.lat" placeholder="请输入纬度" />
                </el-form-item>

                <el-form-item label="经度" prop="lng">
                  <el-input v-model="form.lng" placeholder="请输入经度" />
                </el-form-item>

                <el-form-item label="地点" prop="location">
                  <el-input v-model="form.location" type="textarea" placeholder="请输入内容" />
                </el-form-item>

                <el-form-item label="预测类别" prop="predclass">
                  <el-input v-model="form.predclass" type="textarea" placeholder="请输入内容" />
                </el-form-item>

                <el-form-item label="预测标签" prop="predlabel">
                  <el-input v-model="form.predlabel" type="textarea" placeholder="请输入内容" />
                </el-form-item>

                <el-form-item label="预测分数" prop="predscore">
                  <el-input v-model="form.predscore" placeholder="请输入预测分数" />
                </el-form-item>

                <el-form-item label="上报ID" prop="reportid">
                  <el-input v-model="form.reportid" placeholder="请输入上报ID" />
                </el-form-item>

                <el-form-item label="时间" prop="time">
                  <el-input v-model="form.time" type="textarea" placeholder="请输入内容" />
                </el-form-item>

                <el-form-item label="更新者" prop="updateBy">
                  <el-input v-model="form.updateBy" placeholder="请输入更新者" />
                </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
      <!-- 导入数据对话框 -->
    <ImportData
        v-if="openImport"
        v-model="openImport"
        tableName="history"
        @success="handleImportSuccess"
    />
  </div>
</template>

<script setup name="History">
import { listHistory, getHistory, delHistory, addHistory, updateHistory, importHistory } from "@/api/history/history";
import { listAllTable } from '@/api/system/table'
import TableSetup from '@/components/TableSetup'
import AutoTable from '@/components/AutoTable'
import ImportData from '@/components/ImportData'
const { proxy } = getCurrentInstance();
const { predclass_type } = proxy.useDict('predclass_type');

const historyList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const columns = ref([])
const stripe = ref(true)
const isTable = ref(true)
const tableHeight = ref(500)
const fullScreen = ref(false)
const openImport = ref(false)

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    id: null,
    location: null,
    predclass: null,
    predscore: null,
    reportid: null,
  },
  rules: {
        image: [
          { required: true, message: "图像不能为空", trigger: "blur" }
        ],        lat: [
          { required: true, message: "纬度不能为空", trigger: "blur" }
        ],        lng: [
          { required: true, message: "经度不能为空", trigger: "blur" }
        ],        location: [
          { required: true, message: "地点不能为空", trigger: "blur" }
        ],        predclass: [
          { required: true, message: "预测类别不能为空", trigger: "blur" }
        ],        predlabel: [
          { required: true, message: "预测标签不能为空", trigger: "blur" }
        ],        predscore: [
          { required: true, message: "预测分数不能为空", trigger: "blur" }
        ],        reportid: [
          { required: true, message: "上报ID不能为空", trigger: "blur" }
        ],        time: [
          { required: true, message: "时间不能为空", trigger: "blur" }
        ],  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询history列表 */
function getList() {
  loading.value = true;
  listHistory(queryParams.value).then(response => {
    historyList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

function getColumns() {
    listAllTable({ tableName: 'history' })
        .then((response) => {
            columns.value = response.data
        })
        .then(() => {
            getList()
        })
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
        createBy: null,        createTime: null,        delFlag: null,        deptId: null,        id: null,        image: null,        lat: null,        lng: null,        location: null,        predclass: null,        predlabel: null,        predscore: null,        reportid: null,        time: null,        updateBy: null,        updateTime: null  };
  proxy.resetForm("historyRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加history";
}

/** 新增按钮操作 */
function handleImport() {
    openImport.value = true
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const historyId = row.id || ids.value
  getHistory(historyId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改history";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["historyRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateHistory(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addHistory(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _ids = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除history编号为"' + _ids + '"的数据项？').then(function() {
    return delHistory(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('history/history/export', {
    ...queryParams.value
  }, `history_${new Date().getTime()}.xlsx`)
}

//表格全屏
function onfullTable() {
    proxy.$refs.tSetup.onFull(proxy.$refs.fullTable.$el)
    fullScreen.value = !fullScreen.value
    updateTableHeight()
}
//表格刷新
function onRefresh() {
    getList()
}
//搜索框显示隐藏
function onSearchChange() {
    showSearch.value = !showSearch.value
}

function onStripe(val) {
    stripe.value = val
}
//改变表头数据
function onChange(val) {
    columns.value = val
}

//改变表格宽度
function onColumnWidthChange(column) {
    proxy.$refs.tSetup.tableWidth(column)
}

//更新表格高度
function updateTableHeight() {
    if (
        proxy.$refs.tSetup &&
        proxy.$refs.queryRef &&
        document.querySelector('.table-pagination')
    ) {
        if (fullScreen.value) {
            tableHeight.value = window.innerHeight - 145
        } else {
            tableHeight.value =
                window.innerHeight -
                proxy.$refs.tSetup.$el.clientHeight -
                proxy.$refs.queryRef.$el.clientHeight -
                document.querySelector('.table-pagination').clientHeight -
                220
        }
    }
}
//导入成功
function handleImportSuccess(sheetName, filedInfo, fileName) {
    let data = {
        tableName: 'history',
        filedInfo: filedInfo,
        fileName: fileName,
        sheetName: sheetName
    }
    importHistory(data).then(() => {
        proxy.$modal.msgSuccess('导入成功')
        openImport.value = false
        getList()
    })
    getList()
}

onMounted(() => {
    updateTableHeight() // 初始化计算高度
    window.addEventListener('resize', updateTableHeight) // 监听窗口大小变化
})

onUnmounted(() => {
    window.removeEventListener('resize', updateTableHeight) // 销毁监听
})

getColumns()

</script>