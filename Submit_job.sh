#!/bin/bash
#PBS -N test
#PBS -e /home/ltkoanh/error
#PBS -l nodes=1:ppn=8:super
#PBS -q super

export OMP_NUM_THREADS=8
export basis="sto-6g"

# Thư mục chứa file .xyz
geom_dir="Cluster/Al-B2LYP-6311+Gd-CCSD(T)-xyz"

for xyz_file in "$geom_dir"/*.xyz; do
    mol_name=$(basename "$xyz_file" .xyz)
    echo ">>> Đang xử lý phân tử: $mol_name"

    # Tạo thư mục output
    output_dir="cluster/$mol_name"
    mkdir -p "$output_dir"

    # Copy dữ liệu vào output
    cp "$xyz_file" "$output_dir/${mol_name}.xyz"
    cp cluster/input.py "$output_dir/"

    cd "$output_dir" || exit

    export geom_txt=${mol_name}.xyz

    # Gán spin
    if [[ $mol_name == *"singlet"* ]]; then
        export spin=0
    elif [[ $mol_name == *"doublet"* ]]; then
        export spin=1
    elif [[ $mol_name == *"triplet"* ]]; then
        export spin=2
    elif [[ $mol_name == *"quartet"* ]]; then
        export spin=3
    else
        echo "$mol_name: Không xác định spin"; export spin=0
    fi

    # Gán charge
    if [[ $mol_name == *"anion"* ]]; then
        export charge=-1
    elif [[ $mol_name == *"dianion"* ]]; then
        export charge=-2
    elif [[ $mol_name == *"cation"* ]]; then
        export charge=1
    elif [[ $mol_name == *"neutral"* ]]; then
        export charge=0
    else
        echo "$mol_name: Không xác định charge"; export charge=0
    fi

    echo ">> charge=$charge, spin=$spin"

    # Chạy Python
    python3 input.py > "output-${mol_name}.out"
    echo  "Done $mol_name "

    cd ../../ || exit
done

